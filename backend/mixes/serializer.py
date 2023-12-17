
from django.conf import settings 
from rest_framework import serializers
from .models import Mix


class MixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mix
        fields = ['name','owner','lenght', 'file', 'upload_time']

    