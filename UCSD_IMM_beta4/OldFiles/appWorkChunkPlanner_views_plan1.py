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
    WorkChunk_Plan_Status, \
    WorkChunk_Plan, WorkChunk_Record, \
    WorkChunk_Plan_Form, WorkChunk_Record_Form, \
    WorkChunk_Served, WorkChunk_Served_Form

from WEB.simple_time_selector1 import simple_hh_selector_str, simple_mm_selector_str

@login_required
def plan(request):

    begin_datetime_str  = ""
    begin_date_str      = ""
    begin_time_hh_str   = "09"
    begin_time_mm_str   = "00"       
    finish_datetime_str = ""
    finish_date_str     = ""
    finish_time_hh_str  = "17"
    finish_time_mm_str  = "00"     
    
    time_orient_error_str = ""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        post_intermed = dict([(ikey, request.POST[ikey])
                               for ikey in request.POST])

        begin_date_str      = request.POST.get("begin_date", "")
        begin_time_hh_str   = request.POST.get("begin_time_hh", "09")
        begin_time_mm_str   = request.POST.get("begin_time_mm", "00")
        finish_date_str     = request.POST.get("finish_date", "")
        finish_time_hh_str  = request.POST.get("finish_time_hh", "17")
        finish_time_mm_str  = request.POST.get("finish_time_mm", "00")


        if len(begin_date_str):
            begin_datetime_str  = "%s %s:%s" % (begin_date_str,
                                                begin_time_hh_str,
                                                begin_time_mm_str)
            begin_datetime  = dateutil.parser.parse(begin_datetime_str)
            post_intermed["begin_time"]  = begin_datetime

            
        if len(finish_date_str):
            finish_datetime_str = "%s %s:%s" % (finish_date_str,
                                                finish_time_hh_str,
                                                finish_time_mm_str)
            finish_datetime = dateutil.parser.parse(finish_datetime_str)
            post_intermed["finish_time"] = finish_datetime

        # create a form instance and populate it with data from the request:
        iform = WorkChunk_Plan_Form(post_intermed) # request.POST)
                
        if len(begin_datetime_str) and len(finish_datetime_str):
        
            if begin_datetime >= finish_datetime:
                time_orient_error_str = "<p>Finish time must be after begin finish time</p"
            
            # check whether it's valid:
            elif iform.is_valid():
                # process the data in form.cleaned_data as required
                iform = iform.save(commit=False)
                iform.creator     = request.user
                iform.timestamp   = timezone.now()
                iform.begin_time  = begin_datetime
                iform.finish_time = finish_datetime
                iform.plan_status = WorkChunk_Plan_Status.objects.get(status_name = "Completion expected")
                iform.save()
            
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
          "begin_date_str"         : begin_date_str,
          "finish_date_str"        : finish_date_str,
          "hh_selector_begin_str"  : simple_hh_selector_str(selected = int(begin_time_hh_str),
                                                            no_selection = False),
          "mm_selector_begin_str"  : simple_mm_selector_str(selected = int(begin_time_mm_str),
                                                            no_selection = False),                              
          "hh_selector_finish_str" : simple_hh_selector_str(selected = int(finish_time_hh_str),
                                                            no_selection = False),                             
          "mm_selector_finish_str" : simple_mm_selector_str(selected = int(finish_time_mm_str),
                                                            no_selection = False),
          "time_orient_error_str"  : time_orient_error_str,
        })
    
    templt = loader.get_template("appWorkChunkPlanner/plan3.html")
    return HttpResponse(templt.render(contxt))
  
def plan_info(request, plan_objid):

    wc_recs = WorkChunk_Record.objects.filter(corresp_plan__id = plan_objid)
    sv_evls = WorkChunk_Served.objects.filter(worked_plan__id = plan_objid)

    contxt = RequestContext(request,
        { "wc_recs" : wc_recs,
          "sv_evls" : sv_evls })
    
    templt = loader.get_template("appWorkChunkPlanner/plan_info2.html")
    return HttpResponse(templt.render(contxt))  
  
  
def plan_accept(request, plan_title):
    return HttpResponse("Plan %s accepted!" % plan_title)


def plan_cancel(request, plan_objid, afterwork = ""):
    
    if afterwork:
        afterwork = " after working"
    
    wc_plan = WorkChunk_Plan.objects.get(id = plan_objid) 

    if request.method == 'POST':
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
  
