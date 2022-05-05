#!/usr/bin/env python

'''
Created on 2015/12/21

@author: rsaito
'''

from django.conf.urls import url
from . import views1_9

urlpatterns = [
        # url(r'^testjson/(?P<param1>[a-zA-Z0-9_\-\.]+)/$', views.test_json_ret1, name = "test_json_ret1"),
        url(r'^invoke/$', views1_9.invoke, name = "invoke"),
        url(r'^$',        views1_9.entry,  name = "entry"),
]