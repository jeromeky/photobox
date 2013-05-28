var loadajax;
var currentSizeLoadAjax = 0;

$(document).ready(function(){
	loading(false);
  	fixMenuFolder();
	createLoadAjax();	
	
});

//
// Create jstree of folders
// Need folders list in json
//
function createFolders(jsonTreeFolders){
	$("#treeViewDiv").jstree({
		"json_data" : {
			"data":jsonTreeFolders
		},
		"themes" : {
			"theme" : "classic",
			"dots" : true,
			"icons" : true	
		},
		"plugins" : [ "themes", "json_data", "ui" ]
		}).bind("select_node.jstree", function(e, data){
			Dajaxice.gallery.define_all_images(Dajax.process, {'pathFolder':jQuery.data(data.rslt.obj[0], "href")});
			return data.inst.toggle_node(data.rslt.obj);			
			event.preventDefault();
	});
}


//
// Create swipebox photo
//
function createSwipeImages(){
	$(".swipebox").swipebox();
}

//
// clear then fill gallery with images 
//
function getImageByPage(page){
	Dajaxice.gallery.define_images_by_page(Dajax.process,{'page': page})
}

//
// Create all thumbnail images while a django ajax.
// We make an ajax request for each thumbnail so we can have progression for loader
//
function createGalleryThumbnail(data){
    var obj = jQuery.parseJSON(data);
    currentSizeLoadAjax=0;
	jQuery.each(obj.images, function(index, item) {
		Dajaxice.gallery.create_thumbnail(Dajax.process, {'pathImage':item, 'cpt' : index+1});
	});

}
//
// Fix folders when user scroll
//
function fixMenuFolder(){
/*	jQuery(function($) {
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
	*/
}

function save_settings(){
    Dajaxice.gallery.save_settings(Dajax.process,{'width':$('#width').val(),'height':$('#height').val(),'imagesbypage':$('#imagesbypage').val()})
}

//
// Create loader percentage
//
function createLoadAjax(){
	loadajax = $("#loading").percentageLoader({
	     width : 200, height : 200, progress : 0, value: 40 
     });
}

//
// set progress loader
//
function setProgress(data){
	var obj = jQuery.parseJSON(data);
	loadajax.setProgress(obj.progress);
	console.log(obj.progress*100);
	currentSizeLoadAjax=currentSizeLoadAjax + obj.size;
	loadajax.setValue(currentSizeLoadAjax + 'Kb');
	console.log("loadingbar");
	$("#loadingbar").css( "width", obj.progress*100+'%' );
}
 
//
// Display loader ajax
//
function displayModalLoading(){
	loading(true);
}

//
// Hide loader ajax
//
function hideModalLoading(){
	loading(false);
}

//
// Clear all images and pagination
// 
function clearAllImages(){
	$("#images").empty();
}

//
// 
//
function clearPageImages(){
	console.log("clear images");
	$("#galleryImage").empty();
}

function changeImagesByPage(div){
	$("#listimagesbypage").children().removeClass('btn-primary');
	$(div).addClass('btn-primary');
	console.log($(div).val());
	if($(div).val() == "ALL")
		$("#imagesbypage").val("9999");
	else
		$("#imagesbypage").val($(div).val());
}

//
// show/hide the ajax-loader.gif
//
function loading(start){
	if(start){
		$("#modalLoading").show();
		$('#loadingmodal').modal('show');
	}else{
		$("#modalLoading").hide();
		$('#loadingmodal').modal('hide');
	}
		
} 