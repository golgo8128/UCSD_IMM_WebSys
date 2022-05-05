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

from rs_Python_Pack3_copied.Graph_Packages.Graph_Draw.DrawNetworkX_simple1_9 \
    import DrawNetworkX_simple
from rs_Python_Pack3_copied.General_Packages.FileDirPath.mkdir_on_absent import mkdir_on_absent
from rs_Python_Pack3_copied.General_Packages.FileDirPath.File_Path1 import rs_filepath_info

HWIDTH_DEFAULT  = 5
HHEIGHT_DEFAULT = 5

# DON'T FORGET TO DO USER AUTHENTICATION!!!

def del_edge(request, edge_id, outer_percent = 300):
    
    timezone.activate(get_tzone(request.user))  
        
    # edges_objs = Nichoedge.objects.filter(edge_id = edge_id,
    #                                       obsolete = False)
    
    edge      = NichoEdge.objects.get(id = edge_id)
    edge_oldinfo = edge.generate_obsolete() 
    edge_oldinfo.save()
    
    node_src_x = edge.node_src.pos_x_on_map
    node_src_y = edge.node_src.pos_y_on_map
    node_tgt_x = edge.node_tgt.pos_x_on_map
    node_tgt_y = edge.node_tgt.pos_y_on_map
    center_x   = (node_src_x + node_tgt_x) / 2
    center_y   = (node_src_y + node_tgt_y) / 2
    x_diff_abs = abs(node_tgt_x - node_src_x)
    y_diff_abs = abs(node_tgt_y - node_src_y)
    if y_diff_abs >= x_diff_abs * HHEIGHT_DEFAULT / HWIDTH_DEFAULT:
        y_width = y_diff_abs
        x_width = y_diff_abs * HWIDTH_DEFAULT / HHEIGHT_DEFAULT
    else:
        x_width = x_diff_abs
        y_width = x_diff_abs * HHEIGHT_DEFAULT / HWIDTH_DEFAULT

    range_x = [ center_x - x_width / 2 * outer_percent / 100,
                center_x + x_width / 2 * outer_percent / 100 ]
    range_y = [ center_y - y_width / 2 * outer_percent / 100,
                center_y + y_width / 2 * outer_percent / 100 ]        
    
    if (range_x[1] - range_x[0] == HWIDTH_DEFAULT and
        range_y[1] - range_y[0] == HHEIGHT_DEFAULT):
        fig_face_color = (0.8, 0.8, 0.7)  
    else:
        fig_face_color = (0.8, 0.8, 0.8)    

    node_vis_id_src = edge.node_src.node_vis_id
    node_vis_id_tgt = edge.node_tgt.node_vis_id
    
    edge.delete()
    
    grf = to_networkx_from_rec(update = True)
    image_file = os.path.join(settings.UCSD_IMM_WORKDIR,
                              "Media", "appNichoAnu", "Images",
                              "edges", "%s.png" % edge_id)
    mkdir_on_absent(rs_filepath_info(image_file)[ "foldername" ])
    # http://127.0.0.1:8000/UCSD_IMM_media/appNichoAnu/Images/tmp1.png
    image_url  = '/'.join([ settings.MEDIA_URL.rstrip('/'),
                            "appNichoAnu", "Images", "edges",
                            "%s.png" % edge_id ])                         
    
    drawgrf = DrawNetworkX_simple(grf)
    drawgrf.output_fig_around_region_simple(
        range_x, range_y,
        nodes_central = [ node_vis_id_src,
                          node_vis_id_tgt ],
        node_label_off_num_nodes = 1000,
        figsize = (6, 6),
        fig_face_color = fig_face_color,
        title = "Edge %s - %s deleted" % (node_vis_id_src,
                                          node_vis_id_tgt),
        outfile = image_file)

    
    contxt = RequestContext(request, { "edge"      : edge,
                                       "image_url" : image_url })
    templt = loader.get_template("appNichoAnu/map_Anurag_del_edge1.html")
    
    return HttpResponse(templt.render(contxt)) 



