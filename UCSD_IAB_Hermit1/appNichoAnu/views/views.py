from django.shortcuts import render

# Create your views here.

import os
from datetime import datetime, timedelta
import dateutil.parser

import getpass

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from django.conf import settings
from django.template import RequestContext, loader
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.urls import reverse
from django.shortcuts import render

from ipware.ip import get_ip

from appNichoAnu.models import *
from appNichoAnu.modules.to_networkx1_6 import to_networkx

from UCSD_IAB_Usefuls.Time.timezone1 import get_tzone

from rs_Python_Pack3_copied.General_Packages.FileDirPath.mkdir_on_absent import mkdir_on_absent
from rs_Python_Pack3_copied.General_Packages.FileDirPath.File_Path1 import rs_filepath_info

from rs_Python_Pack3_copied.General_Packages.Usefuls.TimeStamp_HashFile1_1 import TimeStamp_HashFile

client_ip_log_file = os.path.join(settings.UCSD_IAB_WORKDIR,
                                  "Media", "appNichoAnu", "Log",
                                  "client_ip_log1.pkl")

def index(request):

    timezone.activate(get_tzone(request.user))  

    ipaddr = get_ip(request)
    if ipaddr:        
        mkdir_on_absent(rs_filepath_info(client_ip_log_file)[ "foldername" ])
        ip_log = TimeStamp_HashFile(client_ip_log_file)
        ip_log.stamp(ipaddr)

    contxt = { "NichoNode"   : NichoNode,
               "NichoEdge"   : NichoEdge,
               "settings"    : settings,
               "apache_user" : getpass.getuser(),
               "acount_minus_wk3": len(ip_log.get_keys_timerange(timedelta(days = 21), timedelta(days = 14))),
               "acount_minus_wk2": len(ip_log.get_keys_timerange(timedelta(days = 14), timedelta(days =  7))),
               "acount_minus_wk1": len(ip_log.get_keys_timerange(timedelta(days =  7), timedelta(days =  0))),
            } # {{ message|safe }}

    return render(request,
                  "appNichoAnu/map_Anurag1_3.html",
                  contxt)


def pub_db_tools(request):

    return render(request,
                  "appNichoAnu/pub_db_tools1.html",
                  {})

def survey(request):

    return render(request,
                  "appNichoAnu/survey1.html",
                  {})

def member(request):

    return render(request,
                  "appNichoAnu/nichoanu_member1.html",
                  {})

def material_src(request):

    return render(request,
                  "appNichoAnu/material_src1.html",
                  {})
    
def history(request):

    return render(request,
                  "appNichoAnu/history_Anurag1.html",
                  {})

def work_record(request):

    return render(request,
                  "appNichoAnu/work_record_Golgo1.html",
                  {})

def blog(request):

    return render(request,
                  "appNichoAnu/blog1.html",
                  {})

