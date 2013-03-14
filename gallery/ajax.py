#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import glob
import os.path

@dajaxice_register(method='GET')
def searchFilesInFolder(request, pathFolder):
	folders=[]
	images=[]
	for loopPath in glob.glob(pathFolder+'/*'):
		if(os.path.isdir(loopPath)):
			folders.append(loopPath)
		else:
			images.append(loopPath)

	return simplejson.dumps({'folders':folders, 'images':images, 'currentPath' : pathFolder})
