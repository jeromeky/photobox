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


def searchFolder(path):
	folders = {};
	for loopPath in glob.glob(path + '/*'):
		if(os.path.isdir(loopPath)):
			#keyPath = loopPath.replace(path, '')
			folders[loopPath] = searchFolder(loopPath);
			
	if(len(folders) == 0):
		return False;
	return OrderedDict(sorted(folders.items()));

def treeFolders(rootPath):
	folders = searchFolder(settings.MEDIA_IMAGES)
	return defineFolders(folders, rootPath);


def homepage(request, template='index.html'):
	return render_to_response(template, {'treeFolders' : 	simplejson.dumps(treeFolders(settings.MEDIA_IMAGES))})
