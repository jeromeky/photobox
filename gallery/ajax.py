#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.conf import settings
from collections import OrderedDict
from django.template.loader import render_to_string
import glob
import os.path
from sorl.thumbnail import get_thumbnail

@dajaxice_register(method='GET')
def define_all_images(request, pathFolder):
	dajax = Dajax()
	dajax.add_data(simplejson.dumps({'progress':0}), 'setProgress')
	global paginator
	images = []
	for loopPath in glob.glob(pathFolder + '/*'):
		if(os.path.isfile(loopPath)):
			fileName, fileExtension = os.path.splitext(loopPath)
			if(fileExtension.lower() == ".jpg".lower()):
				thumbnailPath = loopPath.replace(settings.MEDIA_ROOT + "/", "")
				images.append(thumbnailPath)
	paginator = Paginator(images, 20)
	
	if(len(images)>0):
		dajax.script("displayModalLoading();")
		dajax.add_data(simplejson.dumps({'images' : images}), 'createGalleryThumbnail')
	else:
		render = render_to_string('components/images.html', {'items' : items, 'root_media_path' : settings.MEDIA_URL, 'thumb_size' : settings.THUMBNAIL_SIZE})
		dajax.assign('#images', 'innerHTML', render)

	
	
	return dajax.json()
    

@dajaxice_register(method='GET')
def create_thumbnail(request, pathImage, cpt):
	dajax = Dajax()
	get_thumbnail(pathImage, settings.THUMBNAIL_SIZE, crop='center')
	dajax.add_data(simplejson.dumps({'progress':round(float(cpt)/paginator.count,2)}), 'setProgress')
	
	size = os.path.getsize(settings.MEDIA_ROOT + pathImage)
	if(paginator.count == cpt):
		items = paginator.page(1)	
		render = render_to_string('components/images.html', {'items' : items, 'root_media_path' : settings.MEDIA_URL, 'thumb_size' : settings.THUMBNAIL_SIZE})
		dajax.assign('#images', 'innerHTML', render)
		dajax.script("loadPrettyPhoto();")
		dajax.script("hideModalLoading();")
	return dajax.json()

##
##	First call to define all images in a folder
##	then we call define_images_by_page to draw all images in index.html
##
@dajaxice_register(method='GET')
def define_images(request, pathFolder):
    dajax = Dajax()
    global paginator
    images = []
    for loopPath in glob.glob(pathFolder + '/*'):
    	if(os.path.isfile(loopPath)):
    		fileName, fileExtension = os.path.splitext(loopPath)
    		if(fileExtension.lower() == ".jpg".lower()):
    			thumbnailPath = loopPath.replace(settings.MEDIA_ROOT + "/", "")
    			print thumbnailPath
    			get_thumbnail(thumbnailPath	, settings.THUMBNAIL_SIZE, crop='center')
    			images.append(thumbnailPath)

    paginator = Paginator(images, 20)
    return define_images_by_page(request, 1);


##
##	Define image in index.html
##
@dajaxice_register(method='GET')
def define_images_by_page(request, page):
    dajax = Dajax()
        
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    
    mapImages = OrderedDict(); 
    for loopImage in items.object_list:
    	thumbnailPath = loopImage.replace(settings.MEDIA_ROOT + "/", "")
    	loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    	mapImages[thumbnailPath] = loopImage

    #render = render_to_string('components/images.html', {'images' : mapImages,'items' : items, 'im' : settings.MEDIA_URL})
    #dajax.assign('#images', 'innerHTML', render)
    #dajax.script("loadPrettyPhoto();")
#    dajax.script("loading(false);")

    return dajax.json()
    
