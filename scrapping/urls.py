from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import index, registration, pushExample

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrapping.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^registration$', registration),
    url(r'^pushExample$', pushExample),
)
