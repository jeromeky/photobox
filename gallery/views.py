#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
import glob 
import os.path

def homepage(request, template='index.html'):
	folders=[]
	images=[]
	for path in glob.glob('/media/images/normal/*'):
		if(os.path.isdir(path)):
			folders.append(path)
		else: 
			images.append(path)
	return render_to_response(template, {'folders':folders, 'images':images, 'imagesPath' : settings.MEDIA_IMAGES})
