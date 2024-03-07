import mimetypes
import os
from pkgutil import resolve_name
import re
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from mutagen.mp3 import MP3
from rest_framework import status

VALID_FILE_TYPES = ["mp3", "wav"]


def is_valid_file(filename) -> bool:
    ext = filename.rpartition(".")[-1]
    return ext in VALID_FILE_TYPES


def get_mix_length_in_sec(mix_file) -> int:
    audio = MP3(mix_file)
    return audio.info.length


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
