from django.conf.urls import url
from django.urls import path

from . import views

app_name = "AccAuth_TZ"

urlpatterns = [
        path(r'', views.entry, name = "entry"),
        path(r'authenticated/',
               views.authenticated,
               name = "authenticated"),
        path(r'logout/', views.getout, name = "getout"),
        path(r'logout_successful/(?P<iusername>\S+)', views.goodbye, name = "goodbye"),
        path(r'test_member_page/',
             views.test_member_page1,
             name = "test_member_page1"),  
]
