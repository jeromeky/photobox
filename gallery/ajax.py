#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.conf import settings
from collections import OrderedDict
from django.template.loader import render_to_string
import glob
import os.path
from sorl.thumbnail import get_thumbnail
from django.core.files.storage import File
from gallery.views import context
import os,sys
import Image

##
## Define all images
##
@dajaxice_register(method='GET')
def define_all_images(request, pathFolder):
	dajax = Dajax()
	dajax.add_data(simplejson.dumps({'progress':0}), 'setProgress')	
	dajax.script("clearAllImages();")
	global paginator
	print context.width
	images = []
	for loopPath in glob.glob(pathFolder + '/*'):
		if(os.path.isfile(loopPath)):
			fileName, fileExtension = os.path.splitext(loopPath)
			if(fileExtension.lower() == ".jpg".lower()):
				imagePath = loopPath.replace(settings.MEDIA_IMAGES , "")
				images.append(imagePath)
	paginator = Paginator(images, context.imagesbypage)
	thumbnailPath = pathFolder.replace(settings.MEDIA_IMAGES , settings.MEDIA_THUMBNAIL)
	if not os.path.isdir(thumbnailPath) :
		os.makedirs(thumbnailPath)
		
	if(len(images)>0):
		dajax.script("displayModalLoading();")
		dajax.add_data(simplejson.dumps({'images' : images}), 'createGalleryThumbnail')
		## Create directory thumbnail if not exist
		##/Users/jeromeky/Documents/media//normal/2013

	return dajax.json()
    
##
## Create all thumbnail
##
@dajaxice_register(method='GET')
def create_thumbnail(request, pathImage, cpt):
	dajax = Dajax()
#	im = get_thumbnail(pathImage, context.getsize(), crop='center')
#	size = os.path.getsize(settings.MEDIA_ROOT + im.url.replace("/media/", ""))/1000
	dajax.add_data(simplejson.dumps({'progress':round(float(cpt)/paginator.count,2)}), 'setProgress')
	print "___ create thumbnail ____"
	print "path image"
	print pathImage
	size = 128, 128
	outfile = settings.MEDIA_THUMBNAIL + pathImage
	print "outfile"
	print outfile
	
	print "infile"
	print settings.MEDIA_IMAGES + pathImage
	if not os.path.exists(outfile):
		print "not exist"
		try : 
			im = Image.open(settings.MEDIA_IMAGES + pathImage)
			im.thumbnail((128, 128), Image.ANTIALIAS)
			im.save(outfile, "JPEG")
		except IOError as e: 
			print "error create file for ", pathImage
			print e
			
	else : 
		print "exist"
	
	print "___ create thumbnail ____"
	
	if(paginator.count == cpt):
		items = paginator.page(1)	
		render = render_to_string('components/images.html', {'items' : items, 'root_media_path' : settings.MEDIA_URL, 'thumb_size' : context.getsize()})
		dajax.assign('#images', 'innerHTML', render)
		dajax.script("createSwipeImages();")
		dajax.script("hideModalLoading();")
	return dajax.json()


##
##	Define image in index.html
##
@dajaxice_register(method='GET')
def define_images_by_page(request, page):
    dajax = Dajax()
    
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)

    render = render_to_string('components/images.html', {'items' : items, 'root_media_path' : settings.MEDIA_URL, 'thumb_size' : context.getsize()})
    dajax.assign('#images', 'innerHTML', render)
    dajax.script("createSwipeImages();")

    return dajax.json()
    

##
##	Define image in index.html
##
@dajaxice_register(method='GET')
def save_settings(request, width, height, imagesbypage):
    dajax = Dajax()
    context.save(width, height, imagesbypage)
    return dajax.json()
    
    
