from django.db import models
from django.contrib.auth.models import User  # new


# Create your models here.
class Mix(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="mix_files/%Y/%m/%d/")
    length_in_sec = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Mixes"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner.username,
            "upload_time": self.upload_time,
            "file": self.file.name,
            "length": self.length_in_sec,
        }
