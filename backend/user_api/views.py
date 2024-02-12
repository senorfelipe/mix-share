import token
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from .models import User, UserProfile

from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

UserModel = get_user_model()
COOKIE_MAX_AGE_IN_SEC = 3600 * 24 * 14  # 14 days


# answer from github to use httponly-cookie for refresh token (https://github.com/jazzband/djangorestframework-simplejwt/issues/71#issuecomment-762927394)
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


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
        key='refresh_token', value=str(refresh), httponly=True, domain="127.0.0.1",
    )
    return response


# Create your views here.
class RegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                response = get_login_response(new_user, status.HTTP_201_CREATED)
                return response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)

        if not user_password:
            raise AuthenticationFailed('A user password is needed.')

        if not email:
            raise AuthenticationFailed('An user email is needed.')

        user_instance = authenticate(username=email, password=user_password)
        if not user_instance:
            raise AuthenticationFailed('Authentication not successful.')

        if user_instance.is_active:
            response = get_login_response(user_instance)
            return response

        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={'message': 'Something went wrong.'}
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        try:
            refresh_token = request.COOKIES.get['refresh_token']
            if refresh_token:
                token = tokens.RefreshToken(refresh_token)
                token.blacklist()
                response = Response('User logged out successfuly', status=status.HTTP_200_OK)
                response.delete_cookie('refresh_token')
                return response
        except tokens.TokenError:
            raise AuthenticationFailed('Invalid Token')


class UserProfileViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
