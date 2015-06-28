from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import index, pages

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^pages$', pages),
)
