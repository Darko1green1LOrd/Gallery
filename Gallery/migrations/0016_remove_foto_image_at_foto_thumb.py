# Generated by Django 4.2.11 on 2024-10-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0015_rename_image_date_foto_image_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foto',
            name='image_at',
        ),
        migrations.AddField(
            model_name='foto',
            name='thumb',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='album_imgs/thumbs/'),
        ),
    ]
