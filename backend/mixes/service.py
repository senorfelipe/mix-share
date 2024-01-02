import os
from mutagen.mp3 import MP3


VALID_FILE_TYPES = ["mp3", "wav"]


def is_valid_file(filename) -> bool:
    ext = filename.rpartition(".")[-1]
    return ext in VALID_FILE_TYPES


def get_mix_length_in_sec(mix_file) -> int:
    audio = MP3(mix_file)
    return audio.info.length
