const getImages = el =>
  [...el.getElementsByTagName('img')].map(img => img.getAttribute('src'));

const getImageElems = el =>
  [...el.getElementsByTagName('img')].map(img => img);

var $this;
var thumbSize = 108;
var $photoContainer;
var $photoContainer;
var $aktContainer;
var $hiddenContainer;
var $photoTitleContainer;
var isPlaying = false;
var isRandrun = false;
var currentPageInd = -1;
var currentPhotoInd = 0;
var maxPages = 1;
var photos;
var playInterval = 2000;
var randInterval = 3000;
var loadHdPhotos = true;
var loadedImages = {};
var preloadingImageCount = 0;

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function startRandom() {
    if (isRandrun || photos.length-1 == 0) return;
    stopPlaying(true)
    isRandrun = true;
    setTimeout(function() {
        playingRandPhoto();
    }, randInterval);
}

function stopRandom() {
    isRandrun = false;
}

function startPlaying() {
    if (isPlaying) return;
    stopRandom()
    isPlaying = true;
    $this.find('.photos-button-play').addClass('pause');
    setTimeout(function() {
        playingNextPhoto();
    }, playInterval);
    $this.find('.photos-messagebox span').css("background-image", "url('/media/assets/play_white.png')");
    $this.find('.photos-messagebox').fadeIn('fast').delay(800).fadeOut('fast');
}

function stopPlaying(hide_display = false) {
    isPlaying = false;
    $this.find('.photos-button-play').removeClass('pause');
    if (!hide_display){
        $this.find('.photos-messagebox span').css("background-image", "url('/media/assets/pause_white.png')");
        $this.find('.photos-messagebox').fadeIn('fast').delay(800).fadeOut('fast');
    }
}

function launchFullScreen(element) {
    $this.find('.photos-button-fullScreen').toggleClass('fullScreen', true);
    if(element.requestFullScreen) {
        element.requestFullScreen();
    } else if(element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if(element.webkitRequestFullScreen) {
        element.webkitRequestFullScreen();
    } else if(element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}

function fullScreenElement() {
    return document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement;
}

function fullScreenEnabled() {
    return document.fullscreenEnabled || document.mozFullScreenEnabled || document.webkitFullscreenEnabled || document.msFullscreenEnabled;
}

function cancelFullScreen() {
    $this.find('.photos-button-fullScreen').toggleClass('fullScreen', false);
    if (document.cancelFullScreen) {
        document.cancelFullScreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen();
    }
}

function pointerEventToXY(e){
    var out = {x:0, y:0};
    if(e.type == 'touchstart' || e.type == 'touchmove' || e.type == 'touchend' || e.type == 'touchcancel'){
        var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
        out.x = touch.pageX;
        out.y = touch.pageY;
    } else if (e.type == 'mousedown' || e.type == 'mouseup' || e.type == 'mousemove' || e.type == 'mouseover'|| e.type=='mouseout' || e.type=='mouseenter' || e.type=='mouseleave') {
        out.x = e.pageX;
        out.y = e.pageY;
    }
    return out;
};

function playingNextPhoto() {
    if (!isPlaying) return;
    if (currentPhotoInd*1 >= photos.length-1) {
        currentPhotoInd = -1;
    }
    loadPhoto(currentPhotoInd*1+1);
    setTimeout(function() {
        playingNextPhoto();
    }, playInterval);
}

function loadRandPhoto() {
    var rand_ing_pos
    while (true) {
        rand_ing_pos = randInt(0,photos.length-1);
        if (rand_ing_pos != currentPhotoInd || photos.length-1 == 0){break;}
    }
    loadPhoto(rand_ing_pos);
}

function playingRandPhoto() {
    if (!isRandrun) return;
    loadRandPhoto()
    setTimeout(function() {
        playingRandPhoto();
    }, randInterval);
}


function preloadNearbyImages(ind) {
    if (photos.length == 0) return;
    ind = ind*1;

    var prevParam = 'src';
    if (ind > 0 && loadHdPhotos) {
        photos[ind-1].hdsrc = photos[ind-1].hasAttribute("data-hdsrc") ? photos[ind-1].dataset.hdsrc : false;
        if (photos[ind-1].hdsrc) prevParam = 'hdsrc';
    }
    if (preloadingImageCount < 6 && ind > 0 && loadedImages[photos[ind-1][prevParam]] == null) {
        preloadingImageCount++;
        loadedImages[photos[ind-1][prevParam]] = 'loading';
        $('<img src="'+photos[ind-1][prevParam]+'" alt="" style="display:none">').appendTo('body').on('load',function() {
            loadedImages[photos[ind-1][prevParam]] = 'loaded';
            $(this).remove();
            preloadingImageCount--;
        });
    }
    var nextParam = 'src';
    if (ind < photos.length-1 && loadHdPhotos) {
        photos[ind+1].hdsrc = photos[ind+1].hasAttribute("data-hdsrc") ? photos[ind+1].dataset.hdsrc : false;
        if (photos[ind+1].hdsrc) nextParam = 'hdsrc';
    }
    if (preloadingImageCount < 6 && ind < photos.length-1 && loadedImages[photos[ind+1][nextParam]] == null) {
        loadedImages[photos[ind+1][nextParam]] = 'loading';
        preloadingImageCount++;
        $('<img src="'+photos[ind+1][nextParam]+'" alt="" style="display:none">').appendTo('body').on('load',function() {
            loadedImages[photos[ind+1][nextParam]] = 'loaded';
            $(this).remove();
            preloadingImageCount--;
        });
    }
}

function loadPhoto(ind, effect) {
    if (!(ind >= 0 && ind < photos.length)) {
        if (ind < 0) {
            $aktContainer.finish().animate({'left': 60},'fast').animate({'left': 0}, 'slow','easeOutBounce');
        }
        if (ind >= photos.length) {
            $aktContainer.finish().animate({'left': -60},'fast').animate({'left': 0}, 'slow','easeOutBounce');
        }
        return;
    }

    ind = ind*1;
    if (!effect) effect = 'fade';

    var photo = photos[ind];
    $aktContainer.finish();
    $hiddenContainer.finish();
    $photoTitleContainer.finish();
    $this.find('.photos-photo-container').addClass('loading-background');
    if (effect == 'fade') {
        $hiddenContainer.css('left',0);
        $aktContainer.css('left',0);
        $aktContainer.fadeOut('slow', function() {
            $(this).find('img').attr('src','');
        });
        $hiddenContainer.find('img').off('load');
        $hiddenContainer.find('img').on('load', function() {
            $this.find('.photos-photo-container').removeClass('loading-background');
            $this.closest('.photos-galleryWindow').toggleClass('loaded',true);
            loadedImages[$(this).attr('src')] = 'loaded';
            switchContainers();
            $aktContainer.fadeIn('slow');

            resizePhoto($(this));
    });
    } else if (effect == 'rollLeft' || effect == 'rollRight') {
        $hiddenContainer.css('left',(effect == 'rollRight' ? -$hiddenContainer.width() : $hiddenContainer.width()));
        $aktContainer.animate({
                'left': (effect == 'rollRight' ? $aktContainer.width() : -$aktContainer.width())
            }, 400, 'easeOutCubic', function() {
                $(this).hide();
                $(this).css('left',0);
                $(this).find('img').attr('src','');
            }
        );
        $hiddenContainer.find('img').off('load');
        $hiddenContainer.find('img').on('load', function() {
            $this.find('.photos-photo-container').removeClass('loading-background');
            loadedImages[$(this).attr('src')] = 'loaded';

            $hiddenContainer.show();
            $hiddenContainer.animate({
                    'left': 0
                }, 400, 'easeOutCubic',
                function() {
                    $photoTitleContainer.fadeIn('slow');
                }
            );
            switchContainers();
            resizePhoto($(this));
        });
    }

    photo.hdsrc = photo.hasAttribute("data-hdsrc") ? photo.dataset.hdsrc : false;
    $hiddenContainer.find('img').attr('src',(photo.hdsrc && loadHdPhotos ? photo.hdsrc : photo.src)).attr('alt',photo.title ? photo.title : ('Photo'+' '+(photo.time ? photo.time : ind+1).toString()));
    $this.find('.photos-button-download').attr('href',(photo.hdsrc && loadHdPhotos ? photo.hdsrc : photo.src));
    $photoTitleContainer.find('span.photos-photo-title-time').html(photo.hasAttribute("data-time") ? photo.dataset.time : "Date not found");
    //$photoTitleContainer.find('span.photos-photo-title-text').html(et2(photo.title ? photo.title : opts.galleryDesc));
    var infoStr = (ind+1).toString() +' / '+photos.length.toString();
    $photoTitleContainer.find('span.photos-photo-title-info').html(infoStr);

    $this.find('.photos-photoList-container .photos-photoThumb').removeClass('selected');
    $this.find('.photos-photoList-container .photos-photoThumb[data-index="'+ind+'"]').addClass('selected');

    currentPhotoInd = ind;

    preloadNearbyImages(currentPhotoInd);

    $this.find('.photos-photoNav-left').toggle(currentPhotoInd > 0);
    $this.find('.photos-photoNav-right').toggle(currentPhotoInd<photos.length-1);
    var photoPage = Math.floor(currentPhotoInd / photosPerPage);
    if (photoPage != currentPageInd) {
        showPage(photoPage);
    }
}

function showPage(ind) {
    var w = $this.find('.photos-photoList-container').width();
    var pos = $this.find('.photos-photoList-scroller').position();
    var maxPos = Math.floor($this.find('.photos-photoList-scroller').width()/w)*(w-1);
    var targetPos = Math.min(0,Math.max(-maxPos,-(ind*w)));

    $this.find('.photos-photoList-scroller').animate({
        'left': targetPos
    }, function() {
        var g=0//unveilThums()
    });

    currentPageInd = ind;

    if (ind >= maxPages-1) {
        $this.find('.photos-photoList-ra').fadeOut('fast');
    } else {
        $this.find('.photos-photoList-ra').fadeIn('fast');
    }

    if (ind <= 0) {
        $this.find('.photos-photoList-la').fadeOut('fast');
    } else {
        $this.find('.photos-photoList-la').fadeIn('fast');
    }
}

function switchContainers() {
    var pom = $aktContainer;
    $aktContainer = $hiddenContainer;
    $hiddenContainer = pom;
}

function resizePhoto($img) {
    $img.css('max-height',$img.parent().height());
    $img.css('max-width',$img.parent().width());
    $img.css('top',Math.max(($img.parent().height() - $img.height())/2,0).toString()+'px');

    var ow = $this.outerWidth();
    var iw = $img.outerWidth();
    if (ow - iw >= 400) {
        $photoTitleContainer.css('max-width',((ow-iw)/2 - 8)+'px');
    } else {
        $photoTitleContainer.css('max-width','100%');
    }
}

function resize(){
    $this.find('.photos-photo-container').height(0);
    var h = $this.height() - ($random_show ? 54 : 178);
    $this.find('.photos-photo-container').height(h);

    $this.find('.photos-photoList-container').css('width','auto');
    var w = $this.find('.photos-photoList-container').width();
    w = Math.floor(w / thumbSize) * thumbSize;
    $this.find('.photos-photoList-container').width(w);

    photosPerPage = Math.floor(w / thumbSize);
    maxPages = Math.ceil(photos.length / photosPerPage);

    resizePhoto($aktContainer.find('img'));
}

jQuery(document).ready(function($) {
    $this = $(this);
    $photoContainer1 = $(this).find('.photos-photo-1');
    $photoContainer2 = $(this).find('.photos-photo-2');
    $aktContainer = $photoContainer1;
    $hiddenContainer = $photoContainer2;
    $photoTitleContainer = $this.find('.photos-photo-title');
    photos = getImageElems($(".photos-photoList-scroller")[0]);
    $random_show = ($(".albumdisplay")[0].dataset.rand.toLowerCase() === 'true')

    resize();
    $(window).on('resize',function() {
        setTimeout(function() {resize()},150);
    });

    $this.find('.photos-button-fullScreen').on('click',function() {
        if (fullScreenElement()) {
            cancelFullScreen();
        } else {
            launchFullScreen($this.find('.albumdisplay').get(0));
        }
    });

    document.addEventListener('fullscreenchange', exitHandler);
    document.addEventListener('webkitfullscreenchange', exitHandler);
    document.addEventListener('mozfullscreenchange', exitHandler);
    document.addEventListener('MSFullscreenChange', exitHandler);

    function exitHandler() {
        if (!document.fullscreenElement && !document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement && fullScreenElement() == null) {
            $this.find('.photos-button-fullScreen').removeClass('fullScreen', true);
        }
    }

    if ($random_show) {
        $this.find('.photos-button-play').hide()
        $this.find('.photos-button-edit').hide()
        $this.find('.photos-photoList').hide()
        $this.find('.photos-controls').find(".photos-photo-title-info").hide()
        $this.find('.photos-photoNav-left').find(".photos-controls").hide()
        $this.find('.photos-photoNav-right').find(".photos-controls").hide()
        loadRandPhoto()
        startRandom()
    }
    else {
        $this.find('.photos-button-play').on('click',function() {
            if (isPlaying) {
                stopPlaying();
            } else {
                startPlaying();
            }
        });

        $(document).on('keyup',function(event) {
            if (event.keyCode == '39' || event.keyCode == '32' || event.keyCode == '13') {
                loadPhoto(currentPhotoInd*1+1,'rollLeft');
            }
            if (event.keyCode == '37') {
                loadPhoto(currentPhotoInd*1-1,'rollRight');
            }
        });

        var touchX = 0;
        var touchY = 0;
        var wasMouseDown = false;
        var wasTouchStart = false;
        $this.find('.photos-photo-container').on('touchstart mousedown', function(event) {
            event.preventDefault();

            wasMouseDown = true;

            if (event.type == 'touchstart') wasTouchStart = true;

            var xy = pointerEventToXY(event);
            var x = xy.x;
            var y = xy.y;

            touchX = x;
            touchY = y;
        });
        $this.find('.photos-photo-container').on('touchend mouseup', function(event) {
            if (isPlaying) {
                wasMouseDown = false;
                wasTouchStart = false;
                stopPlaying();
                return;
            }
            if (!wasMouseDown && !wasTouchStart) return;
            if (wasTouchStart && wasMouseDown) {
                wasMouseDown = false;
                //return;
            }


            event.stopPropagation();
            event.preventDefault();
            $this.find('.photos-controls').show();
            var xy = pointerEventToXY(event);
            var x = xy.x;
            var y = xy.y;

            if (Math.abs(y-touchY) > Math.abs(x-touchX)) {
                return;
            }
            if (x-touchX < -60) {
                loadPhoto(currentPhotoInd*1+1,'rollLeft');
            } else
            if (x-touchX > 60) {
                loadPhoto(currentPhotoInd*1-1,'rollRight');
            }  else {
                if (x < $this.offset().left + $this.width() / 2) {
                    loadPhoto(currentPhotoInd*1-1,'rollRight');
                } else {
                    loadPhoto(currentPhotoInd*1+1,'rollLeft');
                }
            }
            wasMouseDown = false;
            wasTouchStart = false;
        });

        $this.find('.photos-photoList-ra').on('click',function() {
            if (isPlaying) {
                stopPlaying();
                return;
            }
            showPage(currentPageInd*1+1);
        });
        $this.find('.photos-photoList-la').on('click',function() {
            if (isPlaying) {
                stopPlaying();
                return;
            }
            showPage(currentPageInd*1-1);
        });
        $this.find('.photos-photoList-scroller .photos-photoThumb').on('click', function() {
            if (isPlaying) {
                stopPlaying();
                return;
            }
            loadPhoto($(this).attr('data-index'));
        });
        loadPhoto(0)
    }
});
