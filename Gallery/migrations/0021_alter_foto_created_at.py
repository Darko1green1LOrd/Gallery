# Generated by Django 4.2.11 on 2024-10-27 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0020_alter_album_name_alter_foto_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
