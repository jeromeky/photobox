#-*- coding: utf-8 -*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.conf import settings
from collections import OrderedDict
from django.template.loader import render_to_string
from sorl.thumbnail import get_thumbnail
from django.core.files.storage import File
from gallery.views import context
import os,sys
import Image, ImageOps
import glob


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

	thumbnailPath = pathFolder.replace(settings.MEDIA_IMAGES , os.path.join(settings.MEDIA_THUMBNAIL, context.getsize() + '/'))
	## Create directory thumbnail if not exist
	if not os.path.isdir(thumbnailPath) :
		os.makedirs(thumbnailPath)
		
	if(len(images)>0):
		dajax.script("displayModalLoading();")
		dajax.add_data(simplejson.dumps({'images' : images}), 'createGalleryThumbnail')
	return dajax.json()
    
##
## Create all thumbnail
##
@dajaxice_register(method='GET')
def create_thumbnail(request, pathImage, cpt):
	dajax = Dajax()
	dajax.add_data(simplejson.dumps({'progress':round(float(cpt)/paginator.count,2)}), 'setProgress')
	outfile = os.path.join(settings.MEDIA_THUMBNAIL,  context.getsize(), pathImage,)

	if not os.path.exists(outfile):
		try : 
			im = Image.open(settings.MEDIA_IMAGES + pathImage)
			#im.thumbnail([int(context.width), int(context.height)], Image.ANTIALIAS)
			im = ImageOps.fit(im, (int(context.width), int(context.height)), Image.ANTIALIAS)
			im.save(outfile, "JPEG", quality = 50)
		except IOError as e: 
			print "error create file for ", pathImage
			print e

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
    
    
