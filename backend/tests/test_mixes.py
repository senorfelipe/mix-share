import random
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework_simplejwt import tokens
from rest_framework import status

from user_api.models import User
from mixes.models import Mix, Comment
from .utils import create_two_users, create_simple_uploaded_audio_file


class MixTestCase(APITestCase):
    """
    Test proper handling of mix uploads
    """

    def setUp(self) -> None:
        self.test_mp3_audio_to_duration_set = {'test_1.mp3': 6, 'test_2.mp3': 5}
        self.test_wav_audio_to_duration_set = {'test_1.wav': 4, 'test_2.wav': 2}

        self.user_one, self.user_two = create_two_users()
        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_mp3_file_upload_analyses_duration(self) -> None:
        test_file_name, test_file_duration = random.choice(
            list(self.test_mp3_audio_to_duration_set.items())
        )
        mix_data = {
            'owner': self.user_one.pk,
            'title': test_file_name,
            'description': 'this is a test mix',
            'file': create_simple_uploaded_audio_file(test_file_name),
        }

        response = self.client.post('/api/mixes', data=mix_data, format='multipart')
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            test_file_duration, Mix.objects.filter(title=test_file_name).first().length_in_sec
        )

    def test_wav_file_upload_analyses_duration(self) -> None:
        test_file_name, test_file_duration = random.choice(
            list(self.test_wav_audio_to_duration_set.items())
        )
        mix_data = {
            'owner': self.user_one.pk,
            'title': test_file_name,
            'description': 'this is a test mix',
            'file': create_simple_uploaded_audio_file(test_file_name),
        }

        response = self.client.post('/api/mixes', data=mix_data, format='multipart')
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            test_file_duration, Mix.objects.filter(title=test_file_name).first().length_in_sec
        )


class CommentTestCase(APITestCase):
    """
    Test all related functionality to commenting on mixes.
    """

    def setUp(self) -> None:

        self.user_one = User.objects.create(username="user_one", email="user_one@example.org")
        self.user_two = User.objects.create(username="user_two", email="user_two@example.org")
        self.mix = Mix.objects.create(
            owner=self.user_one,
            title="Test Mix",
            description="this is a test mix",
            file=SimpleUploadedFile(name="test mix", content=b"test content"),
            length_in_sec=150,
        )

        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_can_comment(self):
        post_data = {"text": "my test comment"}
        response = self.client.post(path=f"/api/mixes/{self.mix.id}/comments", data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.mix.comments.all().count(), 1)

    def test_user_can_only_modify_own_comment(self):
        comment_user_two = Comment.objects.create(
            author=self.user_two, mix=self.mix, text="comment user 2"
        )

        response = self.client.put(
            path=f"/api/mixes/{self.mix.id}/comments/{comment_user_two.id}",
            data={"text": "update comment"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_comment(self):
        comment_user_one = Comment.objects.create(
            author=self.user_one, mix=self.mix, text="comment user 1"
        )

        response = self.client.delete(
            path=f"/api/mixes/{self.mix.id}/comments/{comment_user_one.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Comment.objects.filter(id=comment_user_one.id).count())
