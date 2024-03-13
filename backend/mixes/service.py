import contextlib
import mimetypes
import os
from pkgutil import resolve_name
import re
import wave
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from mutagen.mp3 import MP3
from rest_framework import status


class AudioAnalysisExeption(Exception):

    def __init__(self, message="During analysis of the audio file an error occurred"):
        self.message = message
        super().__init__(self.message)


class AudioFileAnalyzer:
    """
    Takes an audio file (wav, mp3) as input and calculates its duration.
    
    Parameters: 
        file (filelike)
    Attributes: 
        duration(int)

    """

    VALID_FILE_TYPES = ("mp3", "wav")

    def __init__(self, file) -> None:
        if file is None:
            raise AudioAnalysisExeption(f'Parameter "file" must be given.')
        if not AudioFileAnalyzer.is_valid_file(file=file):
            raise AudioAnalysisExeption(
                f'Given file type is not supported. Supported types are {AudioFileAnalyzer.VALID_FILE_TYPES}.'
            )
        self.file = file
        self._duration = None
        self.calculate_duration()

    @property
    def duration(self):
        return self._duration
        
    def calculate_duration(self) -> None:
        file_ext = self.file.name.rpartition(".")[-1]
        if file_ext == 'mp3':
            self._duration = self.get_mp3_length_in_sec()
        elif file_ext == 'wav':
            self._duration = self.get_wav_length_in_sec()
        return None

    @classmethod
    def is_valid_file(cls, file) -> bool:
        ext = file.name.rpartition(".")[-1]
        return ext in AudioFileAnalyzer.VALID_FILE_TYPES

    def get_mp3_length_in_sec(self) -> int:
        audio = MP3(self.file)
        return audio.info.length

    def get_wav_length_in_sec(self) -> int:
        with contextlib.closing(wave.open(self.file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return int(duration)


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    DEFAULT_BLK_SIZE = 8192

    def __init__(self, filelike, blksize=DEFAULT_BLK_SIZE, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None we're reading the entire file.
            data = self.filelike.read(self.filelike)
            if data:
                return data
            raise StopIteration
        else:
            if self.remaining <= 0:
                raise StopIteration
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration
            self.remaining -= len(data)
            return data


def stream(request, path) -> StreamingHttpResponse:
    """
    Takes a request and a path to a file and streams the content to the client.
    The request can contain an HTTP Range Header for partial content
    """
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else -1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        response = StreamingHttpResponse(
            RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length),
            status=status.HTTP_206_PARTIAL_CONTENT,
            content_type=content_type,
        )
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
    else:
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        response['Content-Length'] = str(size)
    response['Accept-Ranges'] = 'bytes'
    return response
