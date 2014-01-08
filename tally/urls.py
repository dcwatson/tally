from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tally.views',
    url(r'^archives/$', 'archives'),

    url(r'^archive/(?P<slug>[^/]+)/$', 'archive'),
    url(r'^archive/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', 'archive'),
    url(r'^archive/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'archive'),
    url(r'^archive/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', 'archive'),

    url(r'^admin/', include(admin.site.urls)),
)
