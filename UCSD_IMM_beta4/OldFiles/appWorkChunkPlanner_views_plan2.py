from django.shortcuts import render

# Create your views here.

import dateutil.parser

import pytz
from django.utils import timezone
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import WorkChunk_Class, WorkChunk_Type, \
    WorkChunk_Project, \
    WorkChunk_Plan_Status, \
    WorkChunk_Plan, WorkChunk_Record, \
    WorkChunk_Plan_Form, WorkChunk_Record_Form, \
    WorkChunk_Served, WorkChunk_Served_Form, \
    WorkChunk_Plan_Link_Type, WorkChunk_Plan_Link

from .Usefuls1 import TMPTimeKlass, get_tzone_str

from WEB.simple_time_selector1 import simple_hh_selector_str, simple_mm_selector_str

@login_required
def plan(request):

    timezone.activate(pytz.timezone(get_tzone_str()))
    tk = TMPTimeKlass(pytz.timezone(get_tzone_str()))      

    time_orient_error_str = ""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        post_intermed = dict([(ikey, request.POST[ikey])
                               for ikey in request.POST])

        tk.import_post_req(request.POST,
                           keyw_start = "begin",
                           keyw_end   = "finish")
        if tk.start_datetime:
            post_intermed["begin_time"]  = tk.start_datetime
        if tk.end_datetime:
            post_intermed["finish_time"] = tk.end_datetime

        # create a form instance and populate it with data from the request:
        iform = WorkChunk_Plan_Form(post_intermed) # request.POST)
                
        if tk.start_datetime and tk.end_datetime:
        
            if tk.start_datetime >= tk.end_datetime:
                time_orient_error_str = "<p>Finish time must be after begin finish time</p"
            
            # check whether it's valid:
            elif iform.is_valid():
                # process the data in form.cleaned_data as required
                wcplan = iform.save(commit=False)
                wcplan.creator     = request.user
                wcplan.timestamp   = timezone.now()
                wcplan.begin_time  = tk.start_datetime
                wcplan.finish_time = tk.end_datetime
                wcplan.plan_status = WorkChunk_Plan_Status.objects.get(status_name = "Completion expected")
                wcplan.save()
            
                establish_simple_links(wcplan,
                                       post_intermed.get("link_planids_str", "").split(","))
            
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("appWorkChunkPlanner:plan_accept",
                                                    kwargs = { "plan_title" :
                                                                request.POST["plan_title"] }))

    # if a GET (or any other method) we'll create a blank form
    else:
        iform = WorkChunk_Plan_Form()
        
    iform.fields["chunk_class"].queryset = WorkChunk_Class.objects.filter(user = request.user)
    iform.fields["chunk_type"].queryset  = WorkChunk_Type.objects.filter(user = request.user)
    iform.fields["project"].queryset     = WorkChunk_Project.objects.filter(user = request.user)

    contxt = RequestContext(request,
        { "WorkChunk_Plan_Form"    : iform,
          "begin_date_str"         : tk.start_date_str,
          "finish_date_str"        : tk.end_date_str,
          "hh_selector_begin_str"  : simple_hh_selector_str(selected = int(tk.start_time_hh_str),
                                                            no_selection = False),
          "mm_selector_begin_str"  : simple_mm_selector_str(selected = int(tk.start_time_mm_str),
                                                            no_selection = False),                              
          "hh_selector_finish_str" : simple_hh_selector_str(selected = int(tk.end_time_hh_str),
                                                            no_selection = False),                             
          "mm_selector_finish_str" : simple_mm_selector_str(selected = int(tk.end_time_mm_str),
                                                            no_selection = False),
          "time_orient_error_str"  : time_orient_error_str,
        })
    
    templt = loader.get_template("appWorkChunkPlanner/plan3.html")
    return HttpResponse(templt.render(contxt))
  
def plan_info(request, plan_objid):

    timezone.activate(pytz.timezone(get_tzone_str()))

    wc_plan = WorkChunk_Plan.objects.get(id = plan_objid)
    wc_recs = WorkChunk_Record.objects.filter(corresp_plan__id = plan_objid)
    sv_evls = WorkChunk_Served.objects.filter(worked_plan__id = plan_objid)

    contxt = RequestContext(request,
        { "wc_plan" : wc_plan,
          "wc_recs" : wc_recs,
          "sv_evls" : sv_evls })
    
    templt = loader.get_template("appWorkChunkPlanner/plan_info3.html")
    return HttpResponse(templt.render(contxt))  
  
  
def plan_accept(request, plan_title):
    
    return HttpResponse("Plan %s accepted!" % plan_title)


def plan_cancel(request, plan_objid, afterwork = ""):
    
    timezone.activate(pytz.timezone(get_tzone_str()))
        
    if afterwork:
        afterwork = " after working"
    
    wc_plan = WorkChunk_Plan.objects.get(id = plan_objid) 

    if request.method == 'POST':
        if not wc_plan.timestamp_cancel:
             wc_plan.timestamp_cancel = timezone.now()
        wc_plan.plan_cancel_note = request.POST.get("plan_cancel_note", "")
        wc_plan.save()
        return HttpResponse("Plan \"%s\" canceled%s.<br/>Note:<br/>%s" %
                            (str(wc_plan), afterwork,
                             request.POST.get("plan_cancel_note", "")))
    else:
        contxt = RequestContext(request,
                                { "wc_plan" : wc_plan,
                                  "afterwork" : afterwork })
        templt = loader.get_template("appWorkChunkPlanner/plan_cancel1.html")    
        return HttpResponse(templt.render(contxt))  
  
  
def establish_simple_links(planobj, links_arr):

    for planid_raw in links_arr:
        src_planid  = planid_raw.strip()
        if (len(src_planid) and
            WorkChunk_Plan.objects.filter(id = src_planid).exists()):
            src_planobj = WorkChunk_Plan.objects.get(id = src_planid)
            wc_link = WorkChunk_Plan_Link(
                plan_src = src_planobj,
                plan_tgt = planobj,
                link_type = WorkChunk_Plan_Link_Type.objects.get(
                    link_type_name = "Target plan relevant to source plan"))
            wc_link.save()
