from dataclasses import field
from os import read
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'full_name', 'location']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer

    class Meta:
        model: UserModel
        fields = ['email', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
