from django.conf import settings
from rest_framework import serializers

from mixes import service
from .models import Mix
from .service import VALID_FILE_TYPES


class MixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mix
        fields = [
            'name',
            'owner',
            'description',
            'length_in_sec',
            'file',
            'upload_time',
        ]
        read_only_fields = [
            'length_in_sec',
        ]
