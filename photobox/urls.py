from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings
from django.conf.urls import patterns, include
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


urlpatterns = patterns('',
	(r'^gallery/$', 'gallery.views.homepage'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    # Examples:
    # url(r'^$', 'photobox.views.home', name='home'),
    # url(r'^photobox/', include('photobox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
