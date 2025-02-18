jQuery(document).ready(function($) {
    $('.drop-container').each(function(i, obj) {
        $(obj).on('dragover', function(event) {event.preventDefault();});
        $(obj).on('dragenter', function(event) {
            $(obj).addClass("drag-active");
        });
        $(obj).on('dragleave', function(event) {
            $(obj).removeClass("drag-active");
        });
        $(obj).on('drop', function(event) {
            event.preventDefault();
            $(obj).removeClass("drag-active");
            event.dataTransfer = event.originalEvent.dataTransfer;
            $(obj).find("input")[0].files = event.dataTransfer.files
        });
    });
});
