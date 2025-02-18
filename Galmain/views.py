from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from json import load
from PIL import UnidentifiedImageError
import re
from Gallery.models import (
    Album,
    Foto,
)

login_success = "successMSGSPLITTERLogged In."
login_fail = "warningMSGSPLITTERIncorrect Username/Password."
logout_success = "infoMSGSPLITTERLOgged Out."
editor_noauth = "warningMSGSPLITTERYou must Log In to edit the gallery."
editor_noperms = "warningMSGSPLITTERYour account does not have permission to edit the gallery, if you think this is a mistake please contact the Administrator."
scrf_error = "errorMSGSPLITTERVerification error / SCRF token is missing."
scrf_error_folderupload = "errorMSGSPLITTERVerification Error / This error can be caused by uploading a folder."
err_albumexists = "errorMSGSPLITTERAlbum with this name already exists."
err_albumblank = "errorMSGSPLITTERName cannot be empty."
err_albumlong = "errorMSGSPLITTERName is too long."
albumcreated = "successMSGSPLITTERAlbum Created."
photosuploaded = "successMSGSPLITTERPhotos uploaded."
err_photosinvalid = "errorMSGSPLITTERPhoto/s are damaged or arent photos."
albumsdeleted = "successMSGSPLITTERAlbums deleted."
err_albumnotexists = "errorMSGSPLITTERAlbum with this name does not exist."
err_albumnotfound = "errorMSGSPLITTERAlbum not found."
err_nophotosuploaded = "errorMSGSPLITTERNo photos existing so far.."
photosdeleted = "successMSGSPLITTERPhotos deleted."
err_photonotinalbum = "errorMSGSPLITTERPhoto you are trying to delete is not in this album."
photosdatechangd = "successMSGSPLITTERDates for photo changed."
photosmoved = "successMSGSPLITTERPhotos moved."
err_photonotfound = "errorMSGSPLITTERPhoto not found."
err_nophotosingal = "errorMSGSPLITTERTo edit or delete photos you need to add some first."
err_dateempty = "errorMSGSPLITTERYou didnt enter a date."
err_samename = "errorMSGSPLITTERYou cannot change the name to the same as it was."
namechanged = "successMSGSPLITTERName Changed."


# Create your views here

def homepage(request):

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    albums_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()
    for alb in albums[::-1]:
        albums_data[alb] = {}
        all_photos = [each.img for each in imgs if each.album == alb][::-1]
        albums_data[alb]["photoamount"] = len(all_photos)
        thumnail_img = all_photos
        thumnail_img.append(None)
        albums_data[alb]["thumbnailimg"] = thumnail_img[0]
        if len(all_photos)-1 <= 0:del(albums_data[alb])

    context = {
        "onpage":0,
        "is_editor":is_editor,
        "albums_data":albums_data,
    }

    return render(request, "Galmain/main.html", context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, login_success)
            return redirect(homepage)
        else:
            messages.success(request, login_fail)
            return redirect(login_page)
    else:
        context = {
            "onpage":1,
            "is_editor":False,
        }

        return render(request, "Galmain/main.html", context)

def logout_page(request):
    if not request.user.is_authenticated:
        return redirect(homepage)
    if request.method == "POST":
        logout(request)
        messages.success(request, logout_success)
        return redirect(homepage)
    else:
        context = {
            "onpage":2,
            "is_editor":False,
        }

        return render(request, "Galmain/main.html", context)

def editpage(request):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(homepage)

    albums_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()
    for alb in albums[::-1]:
        albums_data[alb] = {}
        all_photos = [each.img for each in imgs if each.album == alb][::-1]
        albums_data[alb]["photoamount"] = len(all_photos)
        thumnail_img = all_photos
        thumnail_img.append(None)
        albums_data[alb]["thumbnailimg"] = thumnail_img[0]

    context = {
        "onpage":3,
        "is_editor":is_editor,
        "albums_data":albums_data,
    }

    return render(request, "Galmain/main.html", context)

def delalbums(request):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(homepage)


    albums = Album.objects.all()

    if request.method == "POST":
        data = request.POST
        albums_todel = data.getlist('selitm')

        for each_album in albums_todel:
            if each_album not in [album.name for album in albums]:
                messages.success(request, err_albumnotexists)
        for each_album in albums_todel:
            Album.objects.filter(name=each_album).delete()
        messages.success(request, albumsdeleted)
        return redirect(editpage)

    albums_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()
    for alb in albums[::-1]:
        albums_data[alb] = {}
        all_photos = [each.img for each in imgs if each.album == alb][::-1]
        albums_data[alb]["photoamount"] = len(all_photos)
        thumnail_img = all_photos
        thumnail_img.append(None)
        albums_data[alb]["thumbnailimg"] = thumnail_img[0]

    context = {
        "onpage":6,
        "is_editor":is_editor,
        "albums_data":albums_data,
    }

    return render(request, "Galmain/main.html", context)

def viewgal(request,galid):

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    randomsel = False

    album_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()
    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
        album_data["name"] = selected_album.name
        all_photos = [each for each in imgs if each.album == selected_album][::-1]
        album_data["images"] = all_photos
        if len(all_photos) <= 0:
            messages.success(request, err_albumnotfound)
            return redirect(homepage)
    elif galid == "random":
        album_data["name"] = "Random View"
        all_photos = [each for each in imgs][::-1]
        print(all_photos)
        album_data["images"] = all_photos
        randomsel = True
        if len(all_photos) <= 0:
            messages.success(request, err_nophotosuploaded)
            return redirect(homepage)
    else:
        messages.success(request, err_albumnotfound)
        return redirect(homepage)

    context = {
        "onpage":0,
        "isgal":True,
        "randomsel":randomsel,
        "galid":galid,
        "album_data":album_data,
        "is_editor":is_editor,
    }

    return render(request, "Galmain/viewalbum.html", context) #main.html

def editgal(request,galid):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    album_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()

    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
        album_data["name"] = selected_album.name
        all_photos = [each for each in imgs if each.album == selected_album][::-1]
        album_data["photoamount"] = len(all_photos)
        album_data["images"] = all_photos
    else:
        messages.success(request, err_albumnotfound)
        return redirect(editpage)

    if request.method == "POST":
        data = request.POST
        addit = True
        galname = data["name"].strip()

        if addit and galname == album_data["name"]:
            messages.success(request, err_samename)
            addit = False
        if addit and galname in [album.name for album in albums]:
            messages.success(request, err_albumexists)
            addit = False
        if addit and galname == "":
            messages.success(request, err_albumblank)
            addit = False
        if addit and len(galname) > 50:
            messages.success(request, err_albumlong)
            addit = False

        if addit:
            curr_alb = [each for each in albums if str(each.id) == galid][0]
            curr_alb.name = galname
            curr_alb.save()
            messages.success(request, namechanged)
            return redirect(editgal,galid)

    context = {
        "onpage":3,
        "isgal":True,
        "galid":galid,
        "album_data":album_data,
        "is_editor":is_editor,
        "namedit":True,
    }

    return render(request, "Galmain/main.html", context)

def editgal_cdate(request,galid):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    album_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()

    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
        album_data["name"] = selected_album.name
        all_photos = [each for each in imgs if each.album == selected_album][::-1]
        album_data["photoamount"] = len(all_photos)
        album_data["images"] = all_photos
    else:
        messages.success(request, err_albumnotfound)
        return redirect(editpage)

    if album_data["photoamount"] <= 0:
        messages.success(request, err_nophotosingal)
        return redirect(editgal,galid)

    if request.method == "POST":
        data = request.POST
        imgs_todel = data.getlist('selitm')

        for each_img in imgs_todel:
            if len([each for each in imgs if str(each.img) == each_img]) <= 0:
                messages.success(request, err_photonotfound)
                return redirect(editgal_cdate,galid)
        if "date" not in data:
            messages.success(request, err_dateempty)
            return redirect(editgal_cdate,galid)

        set_date = data["date"]
        for each_img in imgs_todel:
            curr_img = [each for each in imgs if str(each.img) == each_img][0]
            curr_img.created_at = set_date
            curr_img.save()
        messages.success(request, photosdatechangd)
        return redirect(editgal,galid)

    context = {
        "onpage":6,
        "isgal":True,
        "galid":galid,
        "album_data":album_data,
        "is_editor":is_editor,
        "showdate":True,
    }

    return render(request, "Galmain/main.html", context)

def editgal_move(request,galid):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    album_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()

    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
        album_data["name"] = selected_album.name
        all_photos = [each for each in imgs if each.album == selected_album][::-1]
        album_data["photoamount"] = len(all_photos)
        album_data["images"] = all_photos
    else:
        messages.success(request, err_albumnotfound)
        return redirect(editpage)

    if album_data["photoamount"] <= 0:
        messages.success(request, err_nophotosingal)
        return redirect(editgal,galid)

    if request.method == "POST":
        data = request.POST
        imgs_todel = data.getlist('selitm')

        for each_img in imgs_todel:
            if len([each for each in imgs if str(each.img) == each_img]) <= 0:
                messages.success(request, err_photonotfound)
                return redirect(editgal_move,galid)
        if "album" in data:
            if data["album"] not in [album.name for album in albums]:
                messages.success(request, err_albumnotfound)
                return redirect(editgal_move,galid)
        else:
            messages.success(request, err_albumnotfound)
            return redirect(editgal_move,galid)

        sel_album = [each for each in albums if each.name == data["album"]][0]
        for each_img in imgs_todel:
            curr_img = [each for each in imgs if str(each.img) == each_img][0]
            curr_img.album = sel_album
            curr_img.save()
        messages.success(request, photosmoved)
        return redirect(editgal,galid)

    context = {
        "onpage":6,
        "isgal":True,
        "galid":galid,
        "album_data":album_data,
        "is_editor":is_editor,
        "all_albums":[alb.name for alb in albums if alb.name != galid],
    }

    return render(request, "Galmain/main.html", context)

def editgal_del(request,galid):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    album_data = {}
    albums = Album.objects.all()
    imgs = Foto.objects.all()


    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
        album_data["name"] = selected_album.name
        all_photos = [each for each in imgs if each.album == selected_album][::-1]
        album_data["photoamount"] = len(all_photos)
        album_data["images"] = all_photos
    else:
        messages.success(request, err_albumnotfound)
        return redirect(editpage)

    if album_data["photoamount"] <= 0:
        messages.success(request, err_nophotosingal)
        return redirect(editgal,galid)

    if request.method == "POST":
        data = request.POST
        imgs_todel = data.getlist('selitm')

        for each_img in imgs_todel:
            sel_photo = [each for each in imgs if str(each.img) == each_img]
            if len(sel_photo) >= 1:
                if sel_photo[0].album != selected_album:
                    messages.success(request, err_photonotinalbum)
                    return redirect(editgal_del,galid)
            else:
                messages.success(request, err_photonotfound)
                return redirect(editgal_del,galid)
        for each_img in imgs_todel:
            [each for each in imgs if str(each.img) == each_img][0].delete()
        messages.success(request, photosdeleted)
        return redirect(editgal,galid)

    context = {
        "onpage":6,
        "isgal":True,
        "galid":galid,
        "album_data":album_data,
        "is_editor":is_editor,
    }

    return render(request, "Galmain/main.html", context)

def addgal(request):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    albums = Album.objects.all()

    if request.method == "POST":
        data = request.POST
        addit = True
        galname = data["name"].strip()

        if addit and galname in [album.name for album in albums]:
            messages.success(request, err_albumexists)
            addit = False
        if addit and galname == "":
            messages.success(request, err_albumblank)
            addit = False
        if addit and len(galname) > 50:
            messages.success(request, err_albumlong)
            addit = False


        if addit:
            Album.objects.create(name = galname)
            messages.success(request, albumcreated)
            return redirect(editpage)


    context = {
        "onpage":4,
        "is_editor":is_editor,
    }

    return render(request, "Galmain/main.html", context)

def editgal_add(request,galid):

    if not request.user.is_authenticated:
        messages.success(request, editor_noauth)
        return redirect(login_page)

    user_groups = request.user.groups.values_list('name',flat = True)
    user_groups_as_list = list(user_groups)
    is_editor = True if "Gallery Manager" in user_groups_as_list else False

    if not is_editor:
        messages.success(request, editor_noperms)
        return redirect(viewgal,galid)

    albums = Album.objects.all()

    if galid in [str(album.id) for album in albums]:
        selected_album = albums[[str(album.id) for album in albums].index(galid)]
    else:
        messages.success(request, err_albumnotfound)
        return redirect(editpage)

    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")

        try:
            for image in images:
                photo = Foto.objects.create(
                    album=[album for album in albums if str(album.id) == galid][0],
                    img=image,
                    created_at=data["date"],
                )
            messages.success(request, photosuploaded)
            return redirect(editgal,galid)
        except UnidentifiedImageError:
            messages.success(request, err_photosinvalid)

    context = {
        "onpage":5,
        "galid":galid,
        "galname":selected_album.name,
        "is_editor":is_editor,
    }

    return render(request, "Galmain/main.html", context)

def csrf_failure(request, reason=""):
    referer = request.META.get('HTTP_REFERER')
    if bool(re.search(r"\/edit\/album\/.*\/add$", referer)):
        messages.success(request, scrf_error_folderupload)
        return HttpResponseRedirect(referer)
    else:
        messages.success(request, scrf_error)
        return redirect(homepage)

