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

        var photoamount = 0;


        elems.each(function(i, obj){
            var titleobj = $(obj).find(".album_title").text();
            var photos_toadd = $(obj).find(".imgamount")[0].dataset.amount;
            photoamount += Number(photos_toadd);

            var div = $('<input required name="selitm" type="text" placeholder="Name of selected item" readonly value="'+titleobj+'">')
            div.appendTo(elemholder)
        });
        albumamount = elems.length;

        var phototext = `${photoamount} Phot${(photoamount == 0 || photoamount >= 5) ? "os" : ((photoamount == 1) ? "o" : "os")}`;
        var albumtext = `${albumamount} Album${(albumamount == 0 || albumamount >= 5) ? "s" : ((albumamount == 1) ? "" : "s")}`;
        $(".confirm").find("a").text("Delete "+phototext+" and "+albumtext+" ?");

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

    $("#albums").children().each(function(i, obj){
        $(obj).click(function(){
            togglesel(this,action);
        });
    });
});
