# Generated by Django 5.0 on 2024-02-16 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0002_alter_user_username_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follows',
            name='followee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee', to='user_api.userprofile'),
        ),
        migrations.AlterField(
            model_name='follows',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user_api.userprofile'),
        ),
    ]