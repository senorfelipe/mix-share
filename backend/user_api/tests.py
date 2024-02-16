from django.test import TestCase

from .views import UserFollowView

from .models import Follow, User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework_simplejwt import tokens


# Create your tests here.
class FollowUnfollowTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_one = User.objects.create(username="user_one", email="user_one@example.org")
        self.user_two = User.objects.create(username="user_two", email="user_two@example.org")
        self.profile_one = self.user_one.profile()
        self.profile_two = self.user_two.profile()

        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_can_follow_another_user(self):
        """
        Ensure one user can follow another user
        """

        response = self.client.post(f'/api/user/{self.profile_one.pk}/follow/{self.profile_two.pk}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        follow = self.profile_one.following.get(follower=self.profile_one)
        self.assertEqual(follow.follower, self.profile_one)
