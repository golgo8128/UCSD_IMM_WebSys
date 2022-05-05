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

NODE_RELIABILITY_DEFAULT = 2

def add_node(request):
    
    timezone.activate(get_tzone(request.user))    
    timezone_now = timezone.now()
        
    if request.method == "POST":
        iform_h = dict([(ikey, request.POST[ikey]) for ikey in request.POST])
        node_form = NichoNode_Form(iform_h)
        # node object is already affected at above line???
        # The object is returned with nodeform.save(commit = False)???
        
        if node_form.is_valid():           
            node_newinfo      = node_form.save(commit = False) 
            node_newinfo.user = request.user
            node_newinfo.timestamp = timezone.now()
            node_newinfo.reliability = NODE_RELIABILITY_DEFAULT
            node_newinfo.save()
            to_networkx_from_rec(update = True)
            return HttpResponse("Node added!")
        else:
            from pprint import pprint
            pprint(node_form.errors)
    else:
        node_form = NichoNode_Form()
       
    contxt = RequestContext(request, { "node_form"   : node_form })
    templt = loader.get_template("appNichoAnu/map_Anurag_add_node1.html")
    
    return HttpResponse(templt.render(contxt)) 
    

