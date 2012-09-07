from django.conf.urls.defaults import *
urlpatterns = patterns('puppet_connect',
    url(r'^$', 'views.index', name="puppet-collect-index"),
)
