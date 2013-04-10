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

def searchFolder(path):
	folders = {};
	for loopPath in glob.glob(path + '/*'):
		if(os.path.isdir(loopPath)):
			keyPath = loopPath.replace(path, '')
			folders[keyPath] = searchFolder(loopPath);
			
	if(len(folders) == 0):
		return "";
	return folders;

def defineFolders(folders, viewHTML):
	viewHTML.append("<ul>");
	for key, value in OrderedDict(sorted(folders.items(), key=lambda t: t[0])):
		viewHTML.append("<li><a>" + key + "</li><li>");
		if(value != null):
			viewHTML.append(defineFolders(value, viewHTML));
	viewHTML.append("</ul>");

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
    			images.append(loopPath)

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
    	thumbnailPath = loopImage.replace(settings.MEDIA_IMAGES, settings.MEDIA_IMAGES_THUMBNAIL);
    	thumbnailPath = thumbnailPath.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	mapImages[thumbnailPath] = loopImage;
    	
    render = render_to_string('components/images.html', {'images' : mapImages,'items' : items})
    dajax.assign('#images', 'innerHTML', render)
    dajax.script("loadPrettyPhoto();")
    
    return dajax.json()
    
