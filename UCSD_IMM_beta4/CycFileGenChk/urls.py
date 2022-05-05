#!/usr/bin/env python

from django.conf.urls import url
from . import views

# File name: XXXXX_done.XXXX ???

urlpatterns = [
        url(r'^main/(?P<istamp_core>[a-zA-Z0-9_\-]+)/$',
            views.filecheck, name = "filecheck"),
        url(r'^srv/(?P<istamp_core>[a-zA-Z0-9_\-]+)/$',
            views.filecheck_server, name = "filecheck_server"),
        url(r'^ok/(?P<istamp_core>[a-zA-Z0-9_\-]+)/$',
            views.file_ok, name = "file_ok"),
        url(r'^err/(?P<istamp_core>[a-zA-Z0-9_\-]+)/$',
            views.found_error, name = "found_error"),        
        url(r'^timeout/(?P<istamp_core>[a-zA-Z0-9_\-]+)$',
            views.timeout, name = "timeout"),
               
]
