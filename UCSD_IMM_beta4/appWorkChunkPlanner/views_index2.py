from django.shortcuts import render

# Create your views here.

import datetime

import dateutil.parser

import pytz
from django.utils import timezone
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from .Usefuls1 import get_tzone_str

from .models import WorkChunk_Class, WorkChunk_Type, \
    WorkChunk_Project, \
    WorkChunk_Plan_Status, \
    WorkChunk_Plan, WorkChunk_Record, \
    WorkChunk_Plan_Form, WorkChunk_Record_Form, \
    WorkChunk_Served, WorkChunk_Served_Form

from WEB.simple_time_selector1 import simple_hh_selector_str, simple_mm_selector_str

RECENT_DTIME = datetime.timedelta(days = 3)

@login_required
def index(request):
    
    timezone.activate(pytz.timezone(get_tzone_str()))
    
    planobjs = \
        WorkChunk_Plan.objects.filter(creator = request.user).\
            order_by("begin_time")
            
    planobj_array = []
    for planobj in planobjs:
        if planobj.plan_status == WorkChunk_Plan_Status.objects.get(status_name = "Completed"):
            if timezone.now() - planobj.work_finished_time() < RECENT_DTIME:
                planobj_array.append(planobj) 
        elif planobj.plan_status == WorkChunk_Plan_Status.objects.get(status_name = "Canceled"):
            if timezone.now() - planobj.timestamp_cancel < RECENT_DTIME:
                planobj_array.append(planobj) 
        else:
            planobj_array.append(planobj)
    
    contxt = RequestContext(request,
                            { "planobjs" : planobj_array })
    templt = loader.get_template("appWorkChunkPlanner/index3.html")
    return HttpResponse(templt.render(contxt))

