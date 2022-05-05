from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.fileupload, name = "fileupload"),
        url(r'^done/$', views.fileupload_done, name = "fileupload_done"),
]
