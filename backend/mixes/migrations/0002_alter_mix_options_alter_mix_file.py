# Generated by Django 5.0 on 2023-12-17 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mix',
            options={'verbose_name_plural': 'Mixes'},
        ),
        migrations.AlterField(
            model_name='mix',
            name='file',
            field=models.FileField(upload_to='mix_files/%Y/%m/%d/'),
        ),
    ]
