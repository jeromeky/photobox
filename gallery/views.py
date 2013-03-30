#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from collections import OrderedDict
import glob 
import os.path
from django.utils import simplejson

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


#  {"data":"Yahoo", "metadata":{"href":"http://www.yahoo.com"}},
 #                                            {"data":"Bing", "metadata":{"href":"http://www.bing.com"}},
  #                                           {"data":"Google", "children":[{"data":"Youtube", "metadata":{"href":"http://youtube.com"}},{"data":"Gmail", #"metadata":{"href":"http://www.gmail.com"}},{"data":"Orkut","metadata":{"href":"http://www.orkut.com"}}], "metadata" : {"href":"http://youtube.com"}}
                                            


def searchFolder(path):
	folders = {};
	for loopPath in glob.glob(path + '/*'):
		if(os.path.isdir(loopPath)):
			#keyPath = loopPath.replace(path, '')
			folders[loopPath] = searchFolder(loopPath);
			
	if(len(folders) == 0):
		return False;
	return folders;


def homepage(request, template='index.html'):
	ajaxfolders = searchFolder(settings.MEDIA_IMAGES)
#	print ajaxfolders
	jsonfolders = defineFolders(ajaxfolders, settings.MEDIA_IMAGES)
	print jsonfolders
	return render_to_response(template, {'imagesPath' : settings.MEDIA_IMAGES, 'jsonfolders' : jsonfolders})
