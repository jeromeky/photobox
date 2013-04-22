var loadajax

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].strip();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue =
decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
        return cookieValue;
    }

function requestPage(event) {
    var element = event;//event.element();
    var url = '/'+element.identify()+'/';
    new Ajax.Updater('content', url, {
        method: 'post',
        requestHeaders: {'X-CSRFToken':getCookie('csrftoken') },
    });
}


function loadPrettyPhoto(){
	$(".swipebox").swipebox();
}



//
// clear then fill gallery with images 
//
function getImageByPage(page){
	$("#galleryImage").empty();
	Dajaxice.gallery.define_images_by_page(Dajax.process,{'page': page})
}

function createGalleryThumbnail(data){
    var obj = jQuery.parseJSON(data);
	jQuery.each(obj.images, function(index, item) {
		Dajaxice.gallery.create_thumbnail(Dajax.process, {'pathImage':item, 'cpt' : index+1});
	});

}

//
// Create jstree of folders
// Need folders list in json
//
function createFolders(jsonTreeFolders){
	$("#treeViewDiv").jstree({
		"json_data" : {
			"data":jsonTreeFolders
		},
		
		"plugins" : [ "themes", "json_data", "ui" ]
		}).bind("select_node.jstree", function(e, data){
//			Dajaxice.gallery.define_images(Dajax.process, {'pathFolder':jQuery.data(data.rslt.obj[0], "href")});
			Dajaxice.gallery.define_all_images(Dajax.process, {'pathFolder':jQuery.data(data.rslt.obj[0], "href")});
			event.preventDefault();
			return data.inst.toggle_node(data.rslt.obj);			
	});
}

//
// Fix folders when user scroll
//
function fixMenuFolder(){
	jQuery(function($) {
	    function fixDiv() {
	      var $cache = $('#filemenu'); 
	      if ($(window).scrollTop() > 50 && $(window).width() > 800) 
	        $cache.css({'position': 'fixed', 'top': '10px'}); 
	      else
	        $cache.css({'position': 'relative', 'top': 'auto'});
	    }
	    $(window).scroll(fixDiv);
	    fixDiv();
	});
}

function createLoadAjax(){
	loadajax = $("#loading").percentageLoader({
	        width : 180, height : 180, progress : 0, value: 40 
        });
}

 function setProgress(data){
 	var obj = jQuery.parseJSON(data);
    loadajax.setProgress(obj.progress);
 }
 
 function displayModalLoading(){
	 loading(true);
 }
 
 function hideModalLoading(){
	 loading(false);
 }
 
//
// show/hide the ajax-loader.gif
//
function loading(start){
	if(start){		
//	    loadajax.setProgress(0);
	    $("#modalLoading").show();
	}else
		$("#modalLoading").hide();
} 