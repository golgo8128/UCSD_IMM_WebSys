#!/usr/bin/env python

from django.conf.urls import url
from . import views

urlpatterns = [

        url(r'^enc/(?P<istr>.+)$', views.strenc, name = "strenc"),
        url(r'^dec/(?P<istr>.+)$', views.strdec, name = "strdec"),
        url(r'^conv$', views.strconv, name = "strconv"),
        url(r'^$', views.index, name = "index"),      

]
