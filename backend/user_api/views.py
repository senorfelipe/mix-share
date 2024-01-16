from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from .models import UserProfile

from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

UserModel = get_user_model()


# Create your views here.
class RegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                refresh = tokens.RefreshToken.for_user(new_user)
                data = {'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}
                response = Response(data=data, status=status.HTTP_201_CREATED)
                # response.set_cookie(key='access_token', value=refresh.access_token, httponly=True)
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
            raise AuthenticationFailed('User not found.')

        if user_instance.is_active:
            refresh_token = tokens.RefreshToken.for_user(user_instance)
            access_token = refresh_token.access_token
            response = Response(
                data={
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                }
            )
            return response

        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={'message': 'Something went wrong.'}
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            if refresh_token:
                token = tokens.RefreshToken(refresh_token)
                token.blacklist()
            return Response("User logged out successfuly", status=status.HTTP_200_OK)
        except tokens.TokenError:
            raise AuthenticationFailed("Invalid Token")


class UserProfileViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    # TODO change permission
    permission_classes = [permissions.AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

