# Generated by Django 4.2.11 on 2024-10-24 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0005_alter_foto_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foto',
            name='name',
        ),
    ]
