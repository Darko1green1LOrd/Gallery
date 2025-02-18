from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.core.files import File
from django.utils import timezone
from io import BytesIO
from PIL import Image
from os import path

def make_thumbnail(image, size=(100, 100)):
    """Makes thumbnails of given size from given image"""

    imo = Image.open(image)
    imd = imo.convert('RGB') # convert mode
    im = imd.resize(size) # resize image
    thumb_io = BytesIO() # create a BytesIO object
    im.save(thumb_io, 'JPEG', quality=85) # save image to BytesIO object
    thumbnail = File(thumb_io, name=path.basename(path.normpath(image.name))) # create a django friendly File object
    return thumbnail

# Create your models here.

class Album(models.Model):
    name = models.CharField('Názov', max_length=50, blank = False, null = False, unique = True)

    def __str__(self):
        return self.name

class Foto(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null = True, blank = False)
    img = models.ImageField(null = False, blank = False, upload_to="album_imgs/")
    created_at = models.DateField(default = timezone.now)
    thumb = models.ImageField(editable = False, null = True, blank = True, upload_to="album_imgs/thumbs/")

    def save(self, *args, **kwargs):
        self.thumb = make_thumbnail(self.img)
        try:
            this = Foto.objects.get(id=self.id)
            if (this.img != self.img) and this.img:
                this.img.delete(False)
            if (this.thumb != self.thumb) and this.thumb:
                this.thumb.delete(False)
        except: pass
        super().save(**kwargs)

    def __str__(self):
        return str(self.img)


@receiver(pre_delete, sender=Foto)
def img_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.img:
        instance.img.delete(False)
    if instance.thumb:
        instance.thumb.delete(False)
