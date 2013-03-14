#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
import glob 
import os.path

def homepage(request, template='index.html'):
	return render_to_response(template, {'imagesPath' : settings.MEDIA_IMAGES})
