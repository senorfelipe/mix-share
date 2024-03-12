from xmlrpc.client import DateTime
from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt import tokens
from rest_framework import status

from user_api.models import User, UserProfile
from mixes.models import Mix, Comment
from os import path


# Create your tests here.
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
        comment_user_two = Comment.objects.create(author=self.user_two, mix=self.mix, text="comment user 2")

        response = self.client.put(
            path=f"/api/mixes/{self.mix.id}/comments/{comment_user_two.id}",
            data={"text": "update comment"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_can_delete_comment(self):
        comment_user_one = Comment.objects.create(author=self.user_one, mix=self.mix, text="comment user 1")
        
        response = self.client.delete(path=f"/api/mixes/{self.mix.id}/comments/{comment_user_one.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Comment.objects.filter(id=comment_user_one.id).count())

