from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^archive/(?P<slug>[^/]+)/values/$', 'tally.views.values'),
    url(r'^admin/', include(admin.site.urls)),
)
