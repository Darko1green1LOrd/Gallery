# Generated by Django 4.2.11 on 2024-10-27 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0019_remove_album_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=300, unique=True, verbose_name='Názov'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 10, 27, 12, 43, 11, 509751, tzinfo=datetime.timezone.utc)),
        ),
    ]
