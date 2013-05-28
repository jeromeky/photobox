#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from collections import OrderedDict
from django.utils import simplejson
import glob 
import os.path
from gallery.context import Context

context = Context(os.getcwd() + "/settings.xml")

##
## Search all folder in a path and return a list of folders
## This is a recursive function, started with a root path then will search
## in all children and so on and so forth until there is no more children path
##
def defineFolders(folders, currentPath):
	children =[];
	for key, value in folders.items():
		jsonfolders ={};
		jsonfolders["metadata"] = {"href" : key}
		folderName = key.replace(currentPath, '')
		jsonfolders["data"]=folderName
		if(value):
			jsonfolders["children"] = defineFolders(value, key);
		children.append(jsonfolders);
	return children;

##
## List all folders in a path and return it in a OrderedDict
##
def searchFolder(path):
	folders = {};
	for loopPath in glob.glob(path + '/*'):
		if(os.path.isdir(loopPath)):
			#keyPath = loopPath.replace(path, '')
			folders[loopPath] = searchFolder(loopPath);
			
	if(len(folders) == 0):
		return False;
	return OrderedDict(sorted(folders.items()));


##
## Define homepage view
##
def homepage(request, template='index.html'):
	jsonFolders = defineFolders(searchFolder(settings.MEDIA_IMAGES), settings.MEDIA_IMAGES)
	return render_to_response(template, {'treeFolders' : simplejson.dumps(jsonFolders), 'thumbnail_width' : context.width, 'thumbnail_height' : context.height, "images_by_page" : context.imagesbypage})

