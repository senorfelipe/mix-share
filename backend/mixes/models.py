from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from mixes import service  # new


# Create your models here.
class Mix(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="mix_files/%Y/%m/%d/")
    length_in_sec = models.IntegerField()

    class Meta:
        verbose_name_plural = "Mixes"



