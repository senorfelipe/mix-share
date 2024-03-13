import os
from user_api.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


def create_two_users(username_one='user_one', username_two='user_two') -> tuple[User, User]:
    user_one = User.objects.create(username=username_one, email=f'{username_one}@example.org')
    user_two = User.objects.create(username=username_two, email=f'{username_two}@example.org')
    return user_one, user_two


def create_simple_uploaded_audio_file(file_name) -> SimpleUploadedFile:
    mp3_file_path = os.path.join(os.path.dirname(__file__), 'resources', file_name)
    with open(mp3_file_path, 'rb') as f:
        file_content = f.read()
        return SimpleUploadedFile(file_name, content=file_content, content_type='audio/mp3')
