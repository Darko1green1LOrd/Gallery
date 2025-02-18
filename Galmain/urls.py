"""
URL configuration for Galmain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Galmain.views import (
    homepage,
    login_page,
    logout_page,
    editpage,
    delalbums,
    viewgal,
    editgal,
    editgal_cdate,
    editgal_move,
    editgal_del,
    addgal,
    editgal_add,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="MainPage"),
    path('edit/', editpage, name="EditPage"),
    path('login/', login_page, name="Login"),
    path('logout/', logout_page, name="Logout"),
    path('album/<str:galid>', viewgal, name="ViewAlbum"),
    path('edit/add', addgal, name="AddAlbum"),
    path('edit/del', delalbums, name="DelAlbum"),
    path('edit/album/<str:galid>', editgal, name="EditAlbum"),
    path('edit/album/<str:galid>/add', editgal_add, name="AddAlbumFiles"),
    path('edit/album/<str:galid>/dat', editgal_cdate, name="ChangeDateAlbumFiles"),
    path('edit/album/<str:galid>/mov', editgal_move, name="MoveAlbumFiles"),
    path('edit/album/<str:galid>/del', editgal_del, name="DeleteAlbumFiles"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
