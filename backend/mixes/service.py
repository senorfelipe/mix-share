import contextlib
import logging
import mimetypes
import os
import subprocess
import sys
import json
import re
from typing import List
import wave
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from mutagen.mp3 import MP3
from rest_framework import status

logger = logging.getLogger('mixshare')


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
    logger.info(f"received range header '{range_header}'")
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        logger.info("Range request matched")
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else -1
        logger.info(f'last byte {last_byte}')
        if last_byte >= size or last_byte == -1:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        logger.info(f'Streaming response from {first_byte} with length {length}')
        response = StreamingHttpResponse(
            RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length),
            status=status.HTTP_206_PARTIAL_CONTENT,
            content_type=content_type,
        )
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
    else:
        logger.info("Range request not matched, streaming complete file content.")
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        response['Content-Length'] = str(size)
    response['Accept-Ranges'] = 'bytes'
    return response


class AudioPeakDecoder(object):
    def __init__(self, file) -> None:
        """
        Takes a audio file (mp3, wav) analyzes its peak data and normlizes it.
        Audio file is analyzed by https://github.com/bbc/audiowaveform. Result is taken and normalized.

        Parameters:
            file_name: audio file name (mp3, wav)
        Attributes:
            peaks: the peak data from the file
            normalized_peaks: the normalized peak data from the file

        Implementation inspired from https://wavesurfer.xyz/faq/
        """
        if file is None:
            raise AudioAnalysisExeption(f'Parameter "file" must be given.')
        if not AudioFileAnalyzer.is_valid_file(file=file):
            raise AudioAnalysisExeption(
                f'Given file type is not supported. Supported types are {AudioFileAnalyzer.VALID_FILE_TYPES}.'
            )
        self._file = file
        self._peaks = None
        self._normalized_peaks = None
        self._get_audiowaveform_data()

    @property
    def peaks(self) -> List[int]:
        return self._peaks

    @property
    def normalized_peaks(self) -> List[float]:
        return self._normalized_peaks

    def _get_audiowaveform_data(self) -> None:
        wavedata_json = 'wavedata.json'
        # audiowaveform -i long_clip.mp3 -o long_clip.json --pixels-per-second 20 --bits 8
        command = [
            'audiowaveform',
            '-i',
            self._file.name,
            '-o',
            wavedata_json,
            '--pixels-per-second',
            '20',
            '--bits',
            '8',
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Analyzing audio peak data of file {self._file.name}.")
        output, error = process.communicate()
        if process.returncode != 0:
            logger.error(f"Analyzing audio peak data failed: '{error.decode()}'")
            raise AudioAnalysisExeption("Analyzing the audio peak data resulted in error.")

        with open(wavedata_json, 'r') as f:
            file_content = f.read()
            os.remove(wavedata_json)
            
        json_content = json.loads(file_content)
        self._peaks = json_content["data"]
        self._channels = json_content["channels"]

    def _deinterleave(self, data, channelCount):
        # first step is to separate the values for each audio channel and min/max value pair, hence we get an array with channelCount * 2 arrays
        deinterleaved = [data[idx :: channelCount * 2] for idx in range(channelCount * 2)]
        new_data = []

        # this second step combines each min and max value again in one array so we have one array for each channel
        for ch in range(channelCount):
            idx1 = 2 * ch
            idx2 = 2 * ch + 1
            ch_data = [None] * (len(deinterleaved[idx1]) + len(deinterleaved[idx2]))
            ch_data[::2] = deinterleaved[idx1]
            ch_data[1::2] = deinterleaved[idx2]
            new_data.append(ch_data)
        return new_data

    def calc_normalized_peaks(self):
        # number of decimals to use when rounding the peak value
        digits = 2

        max_val = float(max(self._peaks))
        new_data = []
        for x in self._peaks:
            new_data.append(round(x / max_val, digits))
        # audiowaveform is generating interleaved peak data when using the --split-channels flag, so we have to deinterleave it
        if self._channels > 1:
            deinterleaved_data = self.deinterleave(new_data, self._channels)
            self._normalized_peaks = deinterleaved_data
        else:
            self._normalized_peaks = new_data
