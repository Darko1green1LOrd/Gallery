# Generated by Django 4.2.11 on 2024-10-24 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0003_foto_alter_album_description_alter_album_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Gallery.album'),
        ),
    ]
