#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from collections import OrderedDict
from django.utils import simplejson
import glob 
import os.path
from gallery.context import Context


from xml.dom.minidom import Document

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
#	xmlSettings = ""
#	try:
#		xmlSettings = parse(os.getcwd() + "/s1ettings.xml")
#	except IOError:
#		print "not exist"
#	print xmlSettings
	
	
#	settings.THUMBNAIL_WIDTH = xmlSettings.getElementsByTagName('width')[0].firstChild.nodeValue
#	settings.THUMBNAIL_HEIGHT = xmlSettings.getElementsByTagName('height')[0].firstChild.nodeValue
#	settings.IMAGES_BY_PAGE = xmlSettings.getElementsByTagName('image_by_page')[0].firstChild.nodeValue
	
#	print xmlSettings.getElementsByTagName('width')[0].firstChild.nodeValue
#	xmlSettings.getElementsByTagName('width')[0].firstChild.nodeValue = "300"
#	print xmlSettings.toxml()


#	xmlpath = os.getcwd() + "/settings.xml"
#	print xmlpath
#	context.save("300","300","30")

#	f = open(os.getcwd() + "/settings", "r")
#	customSettings = {}
#	for line in f:
#		print line,
#		listSettings = line.rstrip().split("=")
#		customSettings[listSettings[0]] = listSettings[1]
#	f.close()
#	print customSettings;
#	if "WIDTH" in customSettings:
#		settings.THUMBNAIL_WIDTH = customSettings["WIDTH"]
		
#	if "HEIGHT" in customSettings:
#		settings.THUMBNAIL_HEIGHT = customSettings["HEIGHT"]
		
#	if "IMAGES_BY_PAGE" in customSettings:
#		settings.IMAGE_BY_PAGE = customSettings["IMAGES_BY_PAGE"]
	
#	if Settings.objects.count() == 0:
#		sett = Settings(width=settings.THUMBNAIL_WIDTH, height=settings.THUMBNAIL_HEIGHT, images_by_page=settings.IMAGES_BY_PAGE)
#		sett.save()
#		print "no result"
#	else:
#		print "result"
#		sett = Settings.objects.all[0]
	
#	print sett
#	settings.THUMBNAIL_SIZE = sett.width + "x" + sett.height
#	settings.IMAGES_BY_PAGE = sett.images_by_page
	print "in views"
	print context.imagesbypage
	jsonFolders = defineFolders(searchFolder(settings.MEDIA_IMAGES), settings.MEDIA_IMAGES)
	return render_to_response(template, {'treeFolders' : simplejson.dumps(jsonFolders), 'thumbnail_width' : context.width, 'thumbnail_height' : context.height, "images_by_page" : context.imagesbypage})

