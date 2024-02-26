from cgitb import lookup
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from django.contrib.auth import get_user_model

from .models import UserProfile

UserModel = get_user_model()


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


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    followers = HyperlinkedIdentityField(
        lookup_field="user_id",
        view_name="user-followers",
    )
    class Meta:
        model = UserProfile
        fields = [
            'pk',
            'username',
            'full_name',
            'avatar',
            'bio',
            'location',
            'followers'
        ]
        read_only_fields = ['username']
