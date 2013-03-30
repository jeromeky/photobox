#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
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

@dajaxice_register
def define_breadcrumb(request, pathFolder):
    dajax = Dajax()
    
    mapBreadcrumb = OrderedDict({'home' : settings.MEDIA_IMAGES});

    breadcrumb = pathFolder.replace(settings.MEDIA_IMAGES , '');
    pathBreadcrumb = settings.MEDIA_IMAGES
    
    for loopBreadcrumb in breadcrumb.split('/'):
    	if(loopBreadcrumb != "") :
    		pathBreadcrumb += '/' + loopBreadcrumb
    		mapBreadcrumb[loopBreadcrumb] = pathBreadcrumb
    
    mapBreadcrumb[next(reversed(mapBreadcrumb))] = "";
   
    render = render_to_string('components/breadcrumb.html' , {'breadcrumb' : mapBreadcrumb})
   
    dajax.assign('#breadcrumb', 'innerHTML', render)
    
    return dajax.json()
    
@dajaxice_register
def define_folders_images(request, pathFolder):
    dajax = Dajax()
    images =[];
    for loopPath in glob.glob(pathFolder + '/*'):
    	if(os.path.isfile(loopPath)):
    		fileName, fileExtension = os.path.splitext(loopPath)
    		print fileExtension
    		if(fileExtension.lower() == ".jpg".lower()):
    			images.append(loopPath)
    		
    mapImages = OrderedDict();
    for loopImage in images:
    	thumbnailPath = loopImage.replace(settings.MEDIA_IMAGES, settings.MEDIA_IMAGES_THUMBNAIL);
    	thumbnailPath = thumbnailPath.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
    	mapImages[thumbnailPath] = loopImage;
    	
    
    render = render_to_string('components/images.html' , {'images' : mapImages})
    dajax.assign('#images', 'innerHTML', render)
    
    
    return dajax.json()

@dajaxice_register(method='GET')
def searchFilesInFolder(request, pathFolder):

	#Look folders and images in pathFolder
	folders=[];
	images=[];
	for loopPath in glob.glob(pathFolder+'/*'):
		if(os.path.isdir(loopPath)):
			folders.append(loopPath)
		else:
			images.append(loopPath)

	
	#Create dictonary with all folders in pathFolder
	#Key => Folder Name
	#Value => Path to the folder
	mapFolders = {};
	for loopFolder in folders:
		mapFolders[loopFolder.replace(pathFolder, '')] = loopFolder;
		
	#We add root path
	mapBreadcrumb = OrderedDict({'2011' : settings.MEDIA_IMAGES});
	
	#Createbreadcrumb
	breadcrumb = pathFolder.replace(settings.MEDIA_IMAGES, '');
	pathBreadcrumb = settings.MEDIA_IMAGES
	
	for loopBreadcrumb in breadcrumb.split('/'):
		if(loopBreadcrumb != "") : 
			pathBreadcrumb +=  '/' + loopBreadcrumb
			mapBreadcrumb[loopBreadcrumb] = pathBreadcrumb

	#We remove path for last key, because we don't want a link to the current path.
	mapBreadcrumb[next(reversed(mapBreadcrumb))] = "";

	#Create dictonary with images
	#Key => Thumbnail Image
	#Value => Normal image size
	mapImages = OrderedDict();
	for loopImage in images:
		#We construct media path with settings.
		thumbnailPath = loopImage.replace(settings.MEDIA_IMAGES, settings.MEDIA_IMAGES_THUMBNAIL);
		thumbnailPath = thumbnailPath.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
		loopImage = loopImage.replace(settings.MEDIA_ROOT, settings.MEDIA_URL);
		mapImages[thumbnailPath] = loopImage;
	
	data = OrderedDict();

	return simplejson.dumps({'currentPath' : pathFolder, 'mapFolders' : mapFolders, 'mapBreadcrumb' : mapBreadcrumb, 'mapImages' : mapImages}, sort_keys=True)
