from django.contrib import admin

# Register your models here.

from .models import (
    Album,
    Foto,
)

admin.site.register(Album)
admin.site.register(Foto)
