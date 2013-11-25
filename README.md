Photobox

Photobox is a python web project to show a gallery of images. It can be easily installed on a local or online server with Python. All you have to do is install all the requirements and to set the path locations of images in a configuration file. Then, you can open webpage of Photobox with any browser you have (Mobile / Tablet / Computer). 

The best way to use Photobox is to used it locally, for example in a computer at your home. Then you can navigate through your photos in photobox, with all devices connected into your network. 

You can see an example here of how it's look like here: http://jeromeky.alwaysdata.net/gallery
Please be advise that this website can be slow because the server used is not enought powerful (alwaysdata.net provide free mutual server)

========

Photobox screenshot : 

![Alt text](screen1.png?raw=true)

![Alt text](screen2.png?raw=true)

========
1) Install Django

2) Install dajaxice

3) Install solr-thumbnail

4) Install PIL

5) Install memcached (memcached.org) (code.google.com/memcached/wiki)
	./configure
	make && make test
	sudo make install
	
6) Install client for memcached (ftp://ftp.tummy.com/pub/python-memcached)
	python setup.py install

7) Install photobox
   by copy (or git clone) all files