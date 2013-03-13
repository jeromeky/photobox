#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import glob
import os.path

@dajaxice_register(method='GET')
def searchFilesInFolder(request, folder):
	dossiers=[]
	fichiers=[]
	for path in glob.glob(folder+'/*'):
		if(os.path.isdir(path)):
			dossiers.append(path)
		else:
			fichiers.append(path)

	return simplejson.dumps({'message':'Hello World', 'dossiers':dossiers, 'fichiers':fichiers})
