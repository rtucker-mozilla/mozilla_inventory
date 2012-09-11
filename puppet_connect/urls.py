from django.conf.urls.defaults import *
urlpatterns = patterns('puppet_connect',
    url(r'^$', 'views.index', name="puppet-collect-index"),
    url(r'^history/(?P<fact>.*)/(?P<system_id>\d+)[/]$', 'views.history', name="puppet-collect-fact-history"),
)
