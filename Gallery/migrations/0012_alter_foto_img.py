# Generated by Django 4.2.11 on 2024-10-25 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0011_alter_foto_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='img',
            field=models.ImageField(upload_to='album_imgs/'),
        ),
    ]
