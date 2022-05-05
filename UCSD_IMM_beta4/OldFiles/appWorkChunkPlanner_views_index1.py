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

LAST_N = 5

@login_required
def index(request):
    
    planobjs = \
        WorkChunk_Plan.objects.filter(creator = request.user).\
            order_by("-timestamp")[:LAST_N]    
    wchkobjs = \
        WorkChunk_Record.objects.filter(corresp_plan__creator = request.user).\
            order_by("-timestamp")
    
    contxt = RequestContext(request,
                            { "planobjs" : planobjs,
                              "wchkobjs" : wchkobjs })
    templt = loader.get_template("appWorkChunkPlanner/index2.html")
    return HttpResponse(templt.render(contxt))

