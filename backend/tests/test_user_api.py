from django.test import override_settings

from user_api.views import UserProfileViewSet
from .utils import create_two_users
from user_api.models import Follow, User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import tokens


# Create your tests here.
class FollowUserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_one, self.user_two = create_two_users()
        self.profile_one = self.user_one.profile()
        self.profile_two = self.user_two.profile()

        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_can_follow(self):
        """
        Ensure one user can follow another user
        """
        response = self.client.post(
            f'/api/users/{self.profile_one.pk}/follow/{self.profile_two.pk}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        follow = self.profile_one.following.get(follower=self.profile_one)
        self.assertEqual(follow.follower, self.profile_one)

    def test_follow_unknown_user_results_in_error(self):
        """
        Ensure one can only follow existing users
        """
        not_exisiting_user_id = 99999
        response = self.client.post(
            f'/api/users/{self.profile_one.pk}/follow/{not_exisiting_user_id}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_2 = self.client.post(
            f'/api/users/{not_exisiting_user_id}/follow/{not_exisiting_user_id}'
        )
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)


class UnfollowUserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_one, self.user_two = create_two_users()
        self.profile_one = self.user_one.profile()
        self.profile_two = self.user_two.profile()
        Follow.objects.create(follower=self.profile_one, followee=self.profile_two)

        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_can_unfollow_user(self):
        """
        Ensure user can unfollow user
        """
        self.assertEquals(Follow.objects.count(), 1)
        response = self.client.delete(
            f'/api/users/{self.profile_one.pk}/follow/{self.profile_two.pk}'
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Follow.objects.count(), 0)


class UserProfileTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_one, self.user_two = create_two_users()
        self.profile_one = self.user_one.profile()
        self.profile_two = self.user_two.profile()

        self.factory = APIRequestFactory()
        self.view_profile_detail = UserProfileViewSet.as_view({'get': 'retrieve'})
        self.view_profile_update = UserProfileViewSet.as_view({'patch': 'partial_update'})

        self.token_user_one = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.token_user_two = str(tokens.RefreshToken.for_user(self.user_two).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user_one)

    def test_user_can_view_own_profile(self):
        request = self.factory.get(f'/api/users/{self.profile_one.pk}')
        force_authenticate(request, self.user_one, self.token_user_one)
        response = self.view_profile_detail(request, pk=self.profile_one.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_one.username)

    def test_user_can_update_own_profile(self):
        data = {'location': 'everywhere', 'username': 'John_fucking_Doe'}
        self.assertIsNone(self.profile_one.location)
        request = self.factory.patch(f'/api/users/{self.profile_one.pk}', data=data)
        force_authenticate(request, self.user_one, self.token_user_one)
        response = self.view_profile_update(request, pk=self.profile_one.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile_one.refresh_from_db()
        self.assertEqual(response.data['location'], data['location'])
        self.assertEqual(response.data['username'], data['username'])

    def test_user_can_not_update_other_profile(self):
        data = {'location': 'everywhere', 'username': 'John_fucking_Doe'}
        request = self.factory.patch(f'/api/users/{self.profile_one.pk}', data=data)
        force_authenticate(request, self.user_two)
        response = self.view_profile_update(request, pk=self.profile_one.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.profile_one.location, data['location'])
        self.assertNotEqual(self.profile_one.user.username, data['username'])
