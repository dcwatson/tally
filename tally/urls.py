from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('tally.views',
    url(r'^$', 'index', name='tally-index'),
    url(r'^archive/(?P<slug>[^/]+)/$', 'dashboard', name='tally-archive'),

    url(r'^archives/$', 'archives', name='tally-archives'),

    url(r'^values/(?P<slug>[^/]+)/$', 'data', {'method': 'values'}, name='tally-values'),
    url(r'^values/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', 'data', {'method': 'values'}),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'data', {'method': 'values'}),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', 'data', {'method': 'values'}),

    url(r'^aggregate/(?P<slug>[^/]+)/$', 'data', {'method': 'aggregate'}, name='tally-aggregate'),
    url(r'^aggregate/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', 'data', {'method': 'aggregate'}),
    url(r'^aggregate/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'data', {'method': 'aggregate'}),
    url(r'^aggregate/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', 'data', {'method': 'aggregate'}),

    url(r'^timedata/(?P<slug>[^/]+)/$', 'data', {'method': 'timedata'}, name='tally-timedata'),
    url(r'^timedata/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', 'data', {'method': 'timedata'}),
)

if getattr(settings, 'TALLY_INSTALL_ADMIN', False):
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls))
    )
