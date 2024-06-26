from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from django.contrib.auth import get_user_model
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


UserModel = get_user_model()


# answer from github to use httponly-cookie for refresh token (https://github.com/jazzband/djangorestframework-simplejwt/issues/71#issuecomment-762927394)
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user_password = validated_data.get('password', None)
        db_instance = UserModel.objects.create(
            email=validated_data['email'], username=validated_data['username']
        )
        db_instance.set_password(user_password)
        db_instance.save()
        return db_instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100, read_only=True)
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: UserModel
        fields = ['email', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializerHyperlinkedFollowers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    followers = HyperlinkedIdentityField(
        lookup_field="user_id",
        view_name="user-followers",
    )

    def update(self, instance, validated_data):
        # Update username if provided in the validated data
        user_data = validated_data.pop('user', None)
        if user_data and 'username' in user_data:
            user = instance.user
            user.username = user_data['username']
            user.save()
        return super().update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ['pk', 'username', 'full_name', 'avatar', 'bio', 'location', 'followers']
        read_only_fields = ['username', 'pk']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'pk',
            'username',
            'full_name',
            'avatar',
            'bio',
            'location',
        ]
        read_only_fields = ['username']
