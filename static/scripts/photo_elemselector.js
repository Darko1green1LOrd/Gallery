jQuery(document).ready(function($) {
    $(".preconfirm").click(function(){
        $(".doit").addClass("hidden");
        $(".confirm").removeClass("hidden");
    });

    var action = window.location.href.substring(window.location.href.lastIndexOf('/') + 1)

    function calculate(mode,m="Albums"){
        var elemholder = $(".all_items");
        var elems = $("."+mode+"sel");
        elemholder.empty();

        elems.each(function(i, obj){
            var nameobj = $(obj)[0].dataset.imgn;

            var div = $('<input required name="selitm" type="text" placeholder="Name of selected item" readonly value="'+nameobj+'">')
            div.appendTo(elemholder)
        });

        var photoamount = elems.length;
        var asktext = (mode == "mov") ? "Move " : ((mode == "dat") ? "Change Date " : "Delete ")
        var phototext = `${photoamount} Phot${(photoamount == 0 || photoamount >= 5) ? "os" : ((photoamount == 1) ? "o" : "os")}`;
        $(".confirm").find("a").text(asktext+phototext+" ?");

        if (elems.length > 0) {
            $(".preconfirm").prop("disabled",false);
            $(".confirm").find("button").prop("disabled",false);
        }
        else {
            $(".preconfirm").prop("disabled",true);
            $(".confirm").find("button").prop("disabled",true);
        }
    }

    function togglesel(elem,mode) {
        $(elem).find("div").toggleClass(mode+"sel")
        $(".doit").removeClass("hidden");
        $(".confirm").addClass("hidden");
        calculate(mode);
    }

    $(".album_imgs").children().each(function(i, obj){
        $(obj).click(function(){
            togglesel(this,action);
        });
    });
    $(".preconfirm").html((action == "mov") ? "Move" : ((action == "dat") ? "Change Date" : "Delete"));
    $(".preconfirm").attr("class",`preconfirm ${action+"btn"}`);
    $(".confirm").find("button").attr("class",action+"btn");
});
