from django.contrib import admin

from .models import User, UserProfile


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'location']
