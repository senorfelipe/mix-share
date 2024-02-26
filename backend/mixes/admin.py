from django.contrib import admin

from mixes.models import Comment, Mix


# Register your models here.
@admin.register(Mix)
class MixAdmin(admin.ModelAdmin):
    fields = [
        "owner",
        "name",
        "description",
        "file",
        "length_in_sec",
    ]


@admin.register(Comment)
class MixAdmin(admin.ModelAdmin):
    fields = [
        "author",
        "time",
        "text",
    ]
