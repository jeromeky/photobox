#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import glob 
import os.path 

def homepage(request):
	dossiers=[]
	fichiers=[]
	for path in glob.glob('/media/*'):
		if(os.path.isdir(path)):
			dossiers.append(path)
		else: 
			fichiers.append(path)
	return render_to_response('index.html', {'dossiers':dossiers, 'fichiers':fichiers})
