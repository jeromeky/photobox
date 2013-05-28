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
	jQuery.each(obj.images, function(index, item) {
		Dajaxice.gallery.create_thumbnail(Dajax.process, {'pathImage':item, 'cpt' : index+1});
	});

}

//
// Save custom settings
//
function save_settings(){
    Dajaxice.gallery.save_settings(Dajax.process,{'width':$('#width').val(),'height':$('#height').val(),'imagesbypage':$('#imagesbypage').val()})
}

//
// set progress loader
//
function setProgress(data){
	var obj = jQuery.parseJSON(data);
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
function changeImagesByPage(div){
	$("#listimagesbypage").children().removeClass('btn-primary');
	$(div).addClass('btn-primary');
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