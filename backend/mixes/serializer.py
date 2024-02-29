from os import read
from xml.dom import NotFoundErr
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mixes import service
from .models import Comment, Mix
from .service import VALID_FILE_TYPES


class MixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mix
        fields = [
            'title',
            'owner',
            'description',
            'length_in_sec',
            'file',
            'upload_time',
        ]
        read_only_fields = [
            'length_in_sec',
        ]


class CommentSerializer(serializers.ModelSerializer):
    mix_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'mix_id', 'text', 'username']

    def create(self, validated_data):
        mix_id = self.context["mix_id"]
        mix = get_object_or_404(Mix, id=mix_id)

        author = self.context["request"].user
        text = validated_data.get("text")

        comment = Comment(mix=mix, author=author, text=text)
        comment.save()
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
