#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import glob 
import os.path 

def homepage(request):
	folders=[]
	images=[]
	for path in glob.glob('/media/*'):
		if(os.path.isdir(path)):
			folders.append(path)
		else: 
			images.append(path)
	return render_to_response('index.html', {'folders':folders, 'images':images})
