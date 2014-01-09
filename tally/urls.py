from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tally.views',
    url(r'^archives/$', 'archives'),

    url(r'^values/(?P<slug>[^/]+)/$', 'values'),
    url(r'^values/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', 'values'),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'values'),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', 'values'),

    url(r'^aggregate/(?P<slug>[^/]+)/$', 'aggregate'),
    url(r'^aggregate/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'aggregate'),

    url(r'^admin/', include(admin.site.urls)),
)
