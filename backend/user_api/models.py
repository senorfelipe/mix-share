import imp
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.dispatch import receiver


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def profile(self):
        return UserProfile.objects.get(user=self)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatars', blank=True, null=True)
    bio = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile().save()
