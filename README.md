Photobox

========

need more space raspberry -> http://raspime.com/faq-im-running-out-of-disk-spacehave-insufficient-space-on-my-raspberry-pi-expanding-your-root-file-system/

install pip
 sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 

easy_install pip

Create virtual env :

- virtualenv env2 --no-site-packages
- source env2/bin/activate

MAC OS X --> install with pip

sudo rm -rf /tmp

1) Install DJANGO
- pip install Django


2) Install photobox
   git clone https://github.com/jeromeky/photobox.git

1) Install dajaxice
- sudo pip install django_dajax


3) Install PIL
- sudo pip install PIL

2) Install sorl-thumbnail
- sudo pip install sorl-thumbnail

python manage.py syncdb

4) Install memcached (memcached.org) (http://memcached.org/) (https://code.google.com/p/memcached/wiki/NewStart)
	./configure
	make && make test
	sudo make install
	
	pip install memcached
	
	apt-get install memcached (debian)
	
	memcached -d -m 24 -p 11211
	
5) Install client for memcached (ftp://ftp.tummy.com/pub/python-memcached)
	python setup.py install
	
	sudo pip install python-memcached 


6) install redis

cd deps
make hiredis lua jemalloc lineoise
cd ../
make

(env2)MacBook-Pro-de-Jerome:photobox jeromeky$ pip list
distribute (0.6.36)
Django (1.5)
Pillow (2.0.0)
python-memcached (1.51)
virtualenv (1.9.1)
wsgiref (0.1.2)
