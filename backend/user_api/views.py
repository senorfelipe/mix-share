from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
import logging
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, generics
from rest_framework_simplejwt import tokens
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from .permissions import IsOwnerOfProfileOrRealOnly

from .models import Follow, User, UserProfile

from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileSerializerHyperlinkedFollowers,
    UserRegistrationSerializer,
    CookieTokenRefreshSerializer,
)

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


logger = logging.getLogger('mixshare')
UserModel = get_user_model()
COOKIE_MAX_AGE_IN_SEC = 3600 * 24 * 14  # 14 days


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = COOKIE_MAX_AGE_IN_SEC
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True
            )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = COOKIE_MAX_AGE_IN_SEC
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True
            )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


def get_login_response(user: User, status=status.HTTP_200_OK) -> Response:
    refresh = tokens.RefreshToken.for_user(user)
    data = {'access': str(refresh.access_token)}
    response = Response(data=data, status=status)
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        domain="127.0.0.1",  # TODO fix before production deployment
    )
    return response


# Create your views here.
class RegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        logger.info(f'Registration request for user "{request.data.get("email", None)}"')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                logger.info(f'Registration successful for user "{serializer.validated_data.get("email", None)}"')
                response = get_login_response(new_user, status.HTTP_201_CREATED)
                return response
            logger.warn(f'Registration for user "{request.data.get("email", None)}" failed')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)
        logger.info(f'User "{email}" requests login')

        if not user_password:
            raise AuthenticationFailed('A user password is needed.')

        if not email:
            raise AuthenticationFailed('An user email is needed.')

        user_instance = authenticate(username=email, password=user_password)
        if not user_instance:
            logger.info(f'User: "{email}" could not be authenticated')
            raise AuthenticationFailed('Authentication not successful.')

        if user_instance.is_active:
            logger.info(f'User "{email}" successfully authenticated')
            response = get_login_response(user_instance)
            return response

        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={'message': 'Something went wrong.'}
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = tokens.RefreshToken(refresh_token)
                token.blacklist()
                response = Response('User logged out successfuly', status=status.HTTP_200_OK)
                response.delete_cookie('refresh_token')
                logger.info(f'User "{request.user}" logged out')
                return response
        except tokens.TokenError:
            raise AuthenticationFailed('Invalid Token')


class UserProfileViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfProfileOrRealOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializerHyperlinkedFollowers

    @action(detail=False, methods=['GET'])
    def me(self, request):
        me = UserProfile.objects.get(user=request.user)
        response_data = self.serializer_class(me, context={"request": request}).data
        return Response(status=status.HTTP_200_OK, data=response_data)


class UserFollowView(APIView):

    def post(self, request, follower_id, followee_id):
        try:
            followee_profile = UserProfile.objects.get(id=followee_id)
            follower_profile = UserProfile.objects.get(id=follower_id)
            Follow.objects.create(follower=follower_profile, followee=followee_profile)
            return Response(status=status.HTTP_201_CREATED)
        except UserProfile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "No user exits for given id"}
            )

    def delete(self, request, follower_id, followee_id):
        try:
            followee_profile = UserProfile.objects.get(id=followee_id)
            follower_profile = UserProfile.objects.get(id=follower_id)
            Follow.objects.filter(follower=follower_profile, followee=followee_profile).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "No user exits for given id"}
            )


class FollowersListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(UserProfile, id=user_id)
        follower_ids = [follow.follower.id for follow in user.followers.all()]
        return UserProfile.objects.filter(id__in=follower_ids)
