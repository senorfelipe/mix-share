from django.db import models
from django.contrib.auth.models import User  # new


# Create your models here.
class Mix(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="mixes/%Y/%m/%d/")
    length_in_sec = models.IntegerField(null=True)
