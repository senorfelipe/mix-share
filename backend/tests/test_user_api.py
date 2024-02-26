

from user_api.models import Follow, User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt import tokens


# Create your tests here.
class FollowUserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_one = User.objects.create(username="user_one", email="user_one@example.org")
        self.user_two = User.objects.create(username="user_two", email="user_two@example.org")
        self.profile_one = self.user_one.profile()
        self.profile_two = self.user_two.profile()

        token = str(tokens.RefreshToken.for_user(self.user_one).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_can_follow(self):
        """
        Ensure one user can follow another user
        """
        response = self.client.post(f'/api/users/{self.profile_one.pk}/follow/{self.profile_two.pk}')
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
        self.user_one = User.objects.create(username="user_one", email="user_one@example.org")
        self.user_two = User.objects.create(username="user_two", email="user_two@example.org")
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
