from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.entry, name = "entry"),
        url(r'^authenticated/$',
            views.authenticated,
            name = "authenticated"),
        url(r'^logout/$', views.getout, name = "getout"),
        url(r'^logout_successful/(?P<iusername>\S+)$', views.goodbye, name = "goodbye"),
        url(r'^test_member_page/$',
             views.test_member_page1,
             name = "test_member_page1"),  
]
