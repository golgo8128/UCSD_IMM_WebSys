from django.shortcuts import render

# Create your views here.

import dateutil.parser

import pytz

from django.template import RequestContext, loader
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from .models import WorkChunk_Class, WorkChunk_Type, \
    WorkChunk_Project, \
    WorkChunk_Plan_Status, \
    WorkChunk_Plan, WorkChunk_Record, \
    WorkChunk_Plan_Form, \
    WorkChunk_Record_Form, \
    WorkChunk_Served, WorkChunk_Served_Form
    
from .Usefuls1 import TMPTimeKlass, get_tzone_str

from WEB.simple_time_selector1 import simple_hh_selector_str, simple_mm_selector_str

  
def record(request, plan_objid = None):

    timezone.activate(pytz.timezone(get_tzone_str()))
    tk = TMPTimeKlass(pytz.timezone(get_tzone_str()))   
    time_orient_error_str = ""

    # if this is a POST request we need to process the form data
    resp_redir = None
    if request.method == 'POST':

        post_intermed = dict([(ikey, request.POST[ikey])
                               for ikey in request.POST])

        tk.import_post_req(request.POST)
        if tk.start_datetime:
            post_intermed["start_time"] = tk.start_datetime
        if tk.end_datetime:
            post_intermed["end_time"] = tk.end_datetime

        plan_status_str   = request.POST.get("plan_status", "")

        # create a form instance and populate it with data from the request:
        iform = WorkChunk_Record_Form(post_intermed) # request.POST)
        plan  = WorkChunk_Plan.objects.get(id = iform.data["corresp_plan"])       
        
        if tk.start_datetime and tk.end_datetime:
        
            if tk.start_datetime >= tk.end_datetime:
                time_orient_error_str = "<p>End time must be after start time</p"
            
            # check whether it's valid:
            elif iform.is_valid():
                # process the data in form.cleaned_data as required
                wcrec = iform.save(commit=False)
                wcrec.creator    = request.user
                wcrec.timestamp  = timezone.now()
                wcrec.start_time = tk.start_datetime
                wcrec.end_time   = tk.end_datetime
                wcrec.save()
                                
                plan.plan_status = \
                    WorkChunk_Plan_Status.objects.get(status_name = plan_status_str)
                plan.save()
                
                wc_rec_same_plan = \
                    WorkChunk_Record.objects.filter(corresp_plan = wcrec.corresp_plan)
            
                if plan_status_str == "Canceled":
                    resp_redir = reverse("appWorkChunkPlanner:plan_cancel",
                                         kwargs = { "plan_objid" : plan.id,
                                                    "afterwork"  : "_afterwork" })
                else:
                    resp_redir = reverse("appWorkChunkPlanner:record_accept",
                                         kwargs = { "plan_title" : plan.plan_title,
                                                    "rec_num"    : len(wc_rec_same_plan) })
           
        
        if plan_status_str == "Canceled":
            plan.plan_status = \
                WorkChunk_Plan_Status.objects.get(status_name = plan_status_str)
            plan.timestamp_cancel = timezone.now()
            plan.save()
            if not resp_redir:
                resp_redir = reverse("appWorkChunkPlanner:plan_cancel",
                                     kwargs = { "plan_objid" : plan.id,
                                                "afterwork"  : "" })
                
            
    if resp_redir:
        # redirect to a new URL:
        return HttpResponseRedirect(resp_redir)       
        

    # if a GET (or any other method) we'll create a blank form
    elif plan_objid is not None:
        iform = WorkChunk_Record_Form(initial =
                                      { "corresp_plan" : WorkChunk_Plan.objects.get(id=plan_objid),
                                        "plan_status" : WorkChunk_Plan_Status.objects.get(status_name = "Completion expected")})
    else:
        iform = WorkChunk_Record_Form(initial =
                                      { "plan_status" : WorkChunk_Plan_Status.objects.get(status_name = "Completion expected")})

    iform.fields["corresp_plan"].queryset = WorkChunk_Plan.objects.filter(creator = request.user)

    contxt = RequestContext(request,
        { "WorkChunk_Record_Form" : iform,
          "start_date_str"        : tk.start_date_str,
          "end_date_str"          : tk.end_date_str,
          "hh_selector_start_str" : simple_hh_selector_str(selected = int(tk.start_time_hh_str),
                                                           no_selection = False),
          "mm_selector_start_str" : simple_mm_selector_str(selected = int(tk.start_time_mm_str),
                                                           no_selection = False),                              
          "hh_selector_end_str"   : simple_hh_selector_str(selected = int(tk.end_time_hh_str),
                                                           no_selection = False),                             
          "mm_selector_end_str"   : simple_mm_selector_str(selected = int(tk.end_time_mm_str),
                                                           no_selection = False),
          "time_orient_error_str" : time_orient_error_str,
        })
    
    templt = loader.get_template("appWorkChunkPlanner/record3.html")
    return HttpResponse(templt.render(contxt))


def record_accept(request, plan_title, rec_num):
    
    return HttpResponse("Worked chunk record for plan %s #%s accepted!"
                        % (plan_title, str(rec_num)))
    
    
