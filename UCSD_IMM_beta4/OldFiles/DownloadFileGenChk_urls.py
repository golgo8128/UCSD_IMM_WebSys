#!/usr/bin/env python

from django.conf.urls import url
from . import views1_3

# File name: XXXXX_done.XXXX

urlpatterns = [
        url(r'^main/(?P<istamp>[a-zA-Z0-9_\-]+)/$',
            views1_3.filecheck, name = "filecheck"),
        url(r'^srv/(?P<istamp>[a-zA-Z0-9_\-]+)/$',
            views1_3.filecheck_server, name = "filecheck_server"),
        url(r'^dlpre/(?P<istamp>[a-zA-Z0-9_\-]+)/$',
            views1_3.file_download_pre, name = "file_download_pre"),
        url(r'^dl/(?P<istamp>[a-zA-Z0-9_\-]+)/$',
            views1_3.file_download, name = "file_download"),
        url(r'^err/(?P<istamp>[a-zA-Z0-9_\-]+)/$',
            views1_3.found_error, name = "found_error"),        
        url(r'^timeout/$',
            views1_3.timeout, name = "timeout"),
               
]