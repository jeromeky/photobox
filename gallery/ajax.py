#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.conf import settings
from collections import OrderedDict
from django.template.loader import render_to_string
import glob
import os.path

images = [];

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

def get_range(dictionary, begin, end):
  return dict((k, v) for k, v in dictionary.iteritems() if begin <= k <= end)

@dajaxice_register
def define_images(request, pathFolder):
    dajax = Dajax()
    global images
    images = []
    for loopPath in glob.glob(pathFolder + '/*'):
    	if(os.path.isfile(loopPath)):
    		fileName, fileExtension = os.path.splitext(loopPath)
    		if(fileExtension.lower() == ".jpg".lower()):
    			images.append(loopPath)

    mapImages = OrderedDict();
    for loopImage in images[0:20]:
    	thumbnailPath = loopImage.replace(settings.MEDIA_IMAGES, settings.MEDIA_IMAGES_THUMBNAIL);
    	thumbnailPath = thumbnailPath.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	mapImages[thumbnailPath] = loopImage;
    	
    
    nbPages = range(0, len(images) / 20)
    render = render_to_string('components/images.html' , {'images' : mapImages, 'nbPages' : nbPages, 'currentPage' : 0})
    dajax.assign('#images', 'innerHTML', render)
    
    return dajax.json()
    

@dajaxice_register
def define_images_by_page(request, page):
    dajax = Dajax()
    mapImages = OrderedDict();
    
    firstIndex = int(page)*20;
    print firstIndex
    lastIndex = firstIndex+20;
    
    nbPages = range(0, len(images) / 20)
    
    for loopImage in images[firstIndex:lastIndex]:
    	thumbnailPath = loopImage.replace(settings.MEDIA_IMAGES, settings.MEDIA_IMAGES_THUMBNAIL);
    	thumbnailPath = thumbnailPath.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	mapImages[thumbnailPath] = loopImage;
    	
    render = render_to_string('components/images.html', {'images' : mapImages, 'nbPages' : nbPages, 'currentPage' : page})
    dajax.assign('#images', 'innerHTML', render)
    
    return dajax.json()
    
