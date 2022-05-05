from django.conf.urls import url
from . import views_index2, views_plan3, views_record3, views_serve2

urlpatterns = [

        url(r'^plan_accept/(?P<plan_objid>\d+)$',
            views_plan3.plan_accept, name = "plan_accept"),  
        url(r'^plan/(?P<plan_objid>\d+)/info$',
            views_plan3.plan_info, name = "plan_info"), 
        url(r'^plan/(?P<plan_objid>\d+)/cancel(?P<afterwork>(_afterwork)?)$',
            views_plan3.plan_cancel, name = "plan_cancel"), 
        url(r'^plan$',
            views_plan3.plan, name = "plan"),  
        url(r'^record_accept/(?P<rec_objid>\d+)$',
            views_record3.record_accept, name = "record_accept"), 
        url(r'^record$',
            views_record3.record, name = "record"),  
        url(r'^record/(?P<plan_objid>\d+)$',
            views_record3.record, name = "record"), 
        url(r'^serve_accept/(?P<srv_objid>\d+)',
            views_serve2.serve_accept, name = "serve_accept"), 
        url(r'^serve/(?P<plan_objid>\d+)$',
            views_serve2.serve, name = "serve"), 
        url(r'^serve$',
            views_serve2.serve, name = "serve"), 
        url(r'^$',
            views_index2.index,  name = "index"),      

]
