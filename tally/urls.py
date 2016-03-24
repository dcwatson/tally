from django.conf.urls import include, url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='tally-index'),
    url(r'^archive/(?P<slug>[^/]+)/$', views.dashboard, name='tally-archive'),

    url(r'^archives/$', views.archives, name='tally-archives'),

    url(r'^values/(?P<slug>[^/]+)/$', views.data, {'method': 'values'}, name='tally-values'),
    url(r'^values/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', views.data, {'method': 'values'}),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', views.data, {'method': 'values'}),
    url(r'^values/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', views.data, {'method': 'values'}),

    url(r'^aggregate/(?P<slug>[^/]+)/$', views.data, {'method': 'aggregate'}, name='tally-aggregate'),
    url(r'^aggregate/(?P<slug>[^/]+)/by(?P<by>[^/]+)/$', views.data, {'method': 'aggregate'}),
    url(r'^aggregate/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', views.data, {'method': 'aggregate'}),
    url(r'^aggregate/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/by(?P<by>[^/]+)/$', views.data, {'method': 'aggregate'}),

    url(r'^timedata/(?P<slug>[^/]+)/$', views.data, {'method': 'timedata'}, name='tally-timedata'),
    url(r'^timedata/(?P<slug>[^/]+)/(?P<aggregate>[^/]+)/$', views.data, {'method': 'timedata'}),
]

if getattr(settings, 'TALLY_INSTALL_ADMIN', False):
    from django.contrib import admin
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls))
    ]
