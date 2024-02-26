from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Mix(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="mix_files/%Y/%m/%d/")
    length_in_sec = models.IntegerField()

    class Meta:
        verbose_name_plural = "Mixes"

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f'{self.author}: "{self.text}"'
