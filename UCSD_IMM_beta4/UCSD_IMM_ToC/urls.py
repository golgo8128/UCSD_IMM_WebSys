#!/usr/bin/env python
'''
Created on 2015/12/21

@author: rsaito
'''

from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.entry, name = "entry"),
]
