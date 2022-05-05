from django.shortcuts import render

# Create your views here.

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
   
    
def serve(request, plan_objid = None):
    
    if request.method == 'POST':
        iform = WorkChunk_Served_Form(request.POST)
        if iform.is_valid():
            iform = iform.save(commit=False)
            iform.timestamp = timezone.now()
            iform.save()
            
            srved_same_plan = WorkChunk_Served.objects.filter(worked_plan = iform.worked_plan)
            
            return HttpResponseRedirect(
                reverse("appWorkChunkPlanner:serve_accept",
                        kwargs = { "plan_title"   : iform.worked_plan.plan_title,
                                   "serve_num"    : len(srved_same_plan) }))
            
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

def serve_accept(request, plan_title, serve_num):
    
    return HttpResponse("Contribution of worked plan %s (#%s) accepted!"
                        % (plan_title, str(serve_num)))

