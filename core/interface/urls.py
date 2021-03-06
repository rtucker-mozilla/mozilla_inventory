from django.conf.urls.defaults import patterns, url
from django.views.decorators.csrf import csrf_exempt

from core.interface.static_intr.views import (delete_attr,
        delete_static_interface, edit_static_interface,
        detail_static_interface, quick_create, create_static_interface,
        combine_a_ptr_to_interface, create_no_system_static_interface)

urlpatterns = patterns('',
   url(r'^create/$',
       csrf_exempt(create_no_system_static_interface)),
   url(r'^combine_a_ptr_to_interface/(?P<addr_pk>[\w-]+)/(?P<ptr_pk>[\w-]+)/$',
   csrf_exempt(combine_a_ptr_to_interface)),
   url(r'^(?P<system_pk>[\w-]+)/create/$',
       csrf_exempt(create_static_interface)),
   url(r'^(?P<system_pk>[\w-]+)/quick_create/$',
       csrf_exempt(quick_create)),
   url(r'^(?P<intr_pk>[\w-]+)/$',
       csrf_exempt(detail_static_interface)),
   url(r'^(?P<intr_pk>[\w-]+)/update/$',
       csrf_exempt(edit_static_interface)),
   url(r'^(?P<intr_pk>[\w-]+)/delete/$',
       csrf_exempt(delete_static_interface)),
   url(r'^attr/(?P<attr_pk>[\w-]+)/delete/$',
       csrf_exempt(delete_attr)),
   )
