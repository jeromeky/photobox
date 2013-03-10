#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def homepage(request):

	return render_to_response('index.html', {'data','data'})