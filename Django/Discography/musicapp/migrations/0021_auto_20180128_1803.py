# Generated by Django 2.0.1 on 2018-01-28 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0020_track_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_cover',
            field=models.ImageField(blank=True, upload_to='images/covers/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='track',
            name='audio_file',
            field=models.FileField(blank=True, upload_to='audio/tracks/', verbose_name='Аудио файл'),
        ),
    ]
