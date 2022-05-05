from django.shortcuts import render

# Create your views here.

import os
import dateutil.parser

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from django.conf import settings
from django.template import RequestContext, loader
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect #, JsonResponse
from django.urls import reverse
from appNichoAnu.models import *
from appNichoAnu.modules.to_networkx1_6 import to_networkx_from_rec

from UCSD_IAB_Usefuls.Time.timezone1 import get_tzone

# from Graph_Packages.Graph_Draw.DrawNetworkX_simple1_8 \
#     import DrawNetworkX_simple
# from FileDirPath.mkdir_on_absent import mkdir_on_absent
# from FileDirPath.File_Path1 import rs_filepath_info

HWIDTH_DEFAULT  = 5
HHEIGHT_DEFAULT = 5

EDGE_RELIABILITY_DEFAULT = 2

def add_edge(request):
    
    timezone.activate(get_tzone(request.user))  
            
    if request.method == "POST":
        edge_form = NichoEdge_Form(request.POST)
        # edge object is already affected at above line???
        # The object is returned with edgeform.save(commit = False)???
        
        if edge_form.is_valid():           
            edge_newinfo      = edge_form.save(commit = False) 
            edge_newinfo.user = request.user
            edge_newinfo.timestamp = timezone.now()                           
            edge_newinfo.reliability = EDGE_RELIABILITY_DEFAULT               
            edge_newinfo.save()
            to_networkx_from_rec(update = True)
            return HttpResponse("Modified!")
        else:
            from pprint import pprint
            pprint(edge_form.errors)    
    else:
        edge_form = NichoEdge_Form()                       
    
    contxt = RequestContext(request, { "edge_form" : edge_form })
    templt = loader.get_template("appNichoAnu/map_Anurag_add_edge1.html")
    
    return HttpResponse(templt.render(contxt)) 



