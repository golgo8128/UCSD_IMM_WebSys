from django.shortcuts import render

# Create your views here.

import pytz

import dateutil.parser

from django.template import RequestContext, loader
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from .models import WorkChunk_Class, WorkChunk_Type, \
    WorkChunk_Project, \
    WorkChunk_Plan, WorkChunk_Record, \
    WorkChunk_Plan_Form, WorkChunk_Record_Form, \
    WorkChunk_Served, WorkChunk_Served_Form

from WEB.simple_time_selector1 import simple_hh_selector_str, simple_mm_selector_str

from .Usefuls1 import TMPTimeKlass, get_tzone_str   
    
def serve(request, plan_objid = None):
    
    timezone.activate(pytz.timezone(get_tzone_str()))
    
    if request.method == 'POST':
        iform = WorkChunk_Served_Form(request.POST)
        if iform.is_valid():
            wc_srv = iform.save(commit=False)
            wc_srv.timestamp = timezone.now()
            wc_srv.save()
            
            # srved_same_plan = WorkChunk_Served.objects.filter(worked_plan = wc_srv.worked_plan)
            
            return HttpResponseRedirect(
                reverse("appWorkChunkPlanner:serve_accept",
                        kwargs = { "srv_objid"   : wc_srv.id }))
            
    elif plan_objid is not None:
        iform = WorkChunk_Served_Form(initial =
                                      { "worked_plan" : WorkChunk_Plan.objects.get(id=plan_objid)})        
    else:
        iform = WorkChunk_Served_Form()
        
    iform.fields["worked_plan"].queryset = WorkChunk_Plan.objects.filter(creator = request.user)

    contxt = RequestContext(request,
        { "WorkChunk_Served_Form" : iform })
    templt = loader.get_template("appWorkChunkPlanner/serve1.html")
    
    return HttpResponse(templt.render(contxt)) 

def serve_accept(request, srv_objid):
    
    contxt = RequestContext(request, { })
    templt = loader.get_template("appWorkChunkPlanner/serve_accept1.html")
    return HttpResponse(templt.render(contxt)) 

