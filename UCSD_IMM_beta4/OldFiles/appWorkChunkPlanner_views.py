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


@login_required
def index(request):
    
    contxt = RequestContext(request, {})
    templt = loader.get_template("appWorkChunkPlanner/index1.html")
    return HttpResponse(templt.render(contxt))


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
  
  
def plan_accept(request, plan_title):
    return HttpResponse("Plan %s accepted!" % plan_title)

  
def record(request, plan_objid = None):
    
    start_datetime_str = ""
    start_date_str     = ""
    start_time_hh_str  = "09"
    start_time_mm_str  = "00"       
    end_datetime_str   = ""
    end_date_str       = ""
    end_time_hh_str    = "17"
    end_time_mm_str    = "00"     
    
    time_orient_error_str = ""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        post_intermed = dict([(ikey, request.POST[ikey])
                               for ikey in request.POST])

        start_date_str    = request.POST.get("start_date", "")
        start_time_hh_str = request.POST.get("start_time_hh", "09")
        start_time_mm_str = request.POST.get("start_time_mm", "00")
        end_date_str      = request.POST.get("end_date", "")
        end_time_hh_str   = request.POST.get("end_time_hh", "17")
        end_time_mm_str   = request.POST.get("end_time_mm", "00")


        if len(start_date_str):
            start_datetime_str  = "%s %s:%s" % (start_date_str,
                                                start_time_hh_str,
                                                start_time_mm_str)
            start_datetime  = dateutil.parser.parse(start_datetime_str)
            post_intermed["start_time"]  = start_datetime

            
        if len(end_date_str):
            end_datetime_str = "%s %s:%s" % (end_date_str,
                                             end_time_hh_str,
                                             end_time_mm_str)
            end_datetime = dateutil.parser.parse(end_datetime_str)
            post_intermed["end_time"] = end_datetime

        # create a form instance and populate it with data from the request:
        iform = WorkChunk_Record_Form(post_intermed) # request.POST)
        
        if len(start_datetime_str) and len(end_datetime_str):
        
            if start_datetime >= end_datetime:
                time_orient_error_str = "<p>End time must be after start time</p"
            
            # check whether it's valid:
            elif iform.is_valid():
                # process the data in form.cleaned_data as required
                iform = iform.save(commit=False)
                iform.creator    = request.user
                iform.timestamp  = timezone.now()
                iform.start_time = start_datetime
                iform.end_time   = end_datetime
                iform.save()
                plan   = iform.corresp_plan
                wc_rec_same_plan = WorkChunk_Record.objects.filter(corresp_plan = iform.corresp_plan)
            
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("appWorkChunkPlanner:record_accept",
                                                    kwargs = { "plan_title" : plan.plan_title,
                                                               "rec_num"    : len(wc_rec_same_plan) }))

    # if a GET (or any other method) we'll create a blank form
    elif plan_objid is not None:
        iform = WorkChunk_Record_Form(initial =
                                      { "corresp_plan" : WorkChunk_Plan.objects.get(id=plan_objid)})
    else:
        iform = WorkChunk_Record_Form()

    iform.fields["corresp_plan"].queryset = WorkChunk_Plan.objects.filter(creator = request.user)

    contxt = RequestContext(request,
        { "WorkChunk_Record_Form" : iform,
          "start_date_str"        : start_date_str,
          "end_date_str"          : end_date_str,
          "hh_selector_start_str" : simple_hh_selector_str(selected = int(start_time_hh_str),
                                                           no_selection = False),
          "mm_selector_start_str" : simple_mm_selector_str(selected = int(start_time_mm_str),
                                                           no_selection = False),                              
          "hh_selector_end_str"   : simple_hh_selector_str(selected = int(end_time_hh_str),
                                                           no_selection = False),                             
          "mm_selector_end_str"   : simple_mm_selector_str(selected = int(end_time_mm_str),
                                                           no_selection = False),
          "time_orient_error_str" : time_orient_error_str,
        })
    
    templt = loader.get_template("appWorkChunkPlanner/record1.html")
    return HttpResponse(templt.render(contxt))


def record_accept(request, plan_title, rec_num):
    
    return HttpResponse("Worked chunk record for plan %s #%s accepted!"
                        % (plan_title, str(rec_num)))
    
    
def serve(request, wcrec_objid = None):
    
    if request.method == 'POST':
        iform = WorkChunk_Served_Form(request.POST)
        if iform.is_valid():
            iform = iform.save(commit=False)
            iform.timestamp = timezone.now()
            iform.save()
            
            srved_same_workchunk = WorkChunk_Served.objects.filter(worked_chunk = iform.worked_chunk)
            wc_same_proj         = WorkChunk_Record.objects.filter(corresp_plan = iform.worked_chunk.corresp_plan)
            
            return HttpResponseRedirect(
                reverse("appWorkChunkPlanner:serve_accept",
                        kwargs = { "plan_title"   : iform.worked_chunk.corresp_plan.plan_title,
                                   "plan_rec_num" : len(wc_same_proj),
                                   "serve_num"    : len(srved_same_workchunk) }))
            
    elif wcrec_objid is not None:
        iform = WorkChunk_Served_Form(initial =
                                      { "worked_chunk" : WorkChunk_Record.objects.get(id=wcrec_objid)})        
    else:
        iform = WorkChunk_Served_Form()
        
    iform.fields["worked_chunk"].queryset = WorkChunk_Record.objects.filter(corresp_plan__creator = request.user)

    contxt = RequestContext(request,
        { "WorkChunk_Served_Form" : iform })
    templt = loader.get_template("appWorkChunkPlanner/serve1.html")
    
    return HttpResponse(templt.render(contxt)) 

def serve_accept(request, plan_title, plan_rec_num, serve_num):
    return HttpResponse("Contribution of worked chunk (plan %s #%s) #%s accepted!"
                        % (plan_title, str(plan_rec_num), str(serve_num)))

