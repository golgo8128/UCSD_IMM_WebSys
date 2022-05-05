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

def del_node(request, node_vis_id,
             hwidth  = HWIDTH_DEFAULT,
             hheight = HHEIGHT_DEFAULT,
             offx = 0, offy = 0):
    
    hwidth  = int(hwidth)
    hheight = int(hheight)
    offx    = int(offx)
    offy    = int(offy)
    
    timezone.activate(get_tzone(request.user))    
    timezone_now = timezone.now()
    node = NichoNode.objects.get(node_vis_id = node_vis_id) 
    node_pos_x = node.pos_x_on_map
    node_pos_y = node.pos_y_on_map

    node_oldinfo = node.generate_obsolete(timezone_now)
    node_oldinfo.save()
    edges_deleted_str = []
    for edge in node.assoc_edges():
        edge_oldinfo = edge.generate_obsolete(timezone_now)
        edge_oldinfo.save()
        edges_deleted_str = str(edge)
        edge.delete()

    node.delete()
    
    grf = to_networkx_from_rec(update = True)
    image_file = os.path.join(settings.UCSD_IMM_WORKDIR,
                              "Media", "appNichoAnu", "Images",
                              "nodes", "%s.png" % node_vis_id)
    mkdir_on_absent(rs_filepath_info(image_file)[ "foldername" ])
    # http://127.0.0.1:8000/UCSD_IMM_media/appNichoAnu/Images/tmp1.png
    image_url  = '/'.join([ settings.MEDIA_URL.rstrip('/'),
                            "appNichoAnu", "Images", "nodes",
                            "%s.png" % node_vis_id ])                         
    
    drawgrf = DrawNetworkX_simple(grf)
    if hwidth == HWIDTH_DEFAULT and hheight == HHEIGHT_DEFAULT:
        fig_face_color = (0.8, 0.8, 0.7)  
    else:
        fig_face_color = (0.8, 0.8, 0.8)          
    nodes_drawn, edges_drawn = \
        drawgrf.output_fig_around_region_simple(
            [node_pos_x - hwidth  + offx, node_pos_x + hwidth  + offx],
            [node_pos_y - hheight + offy, node_pos_y + hheight + offy],
            nodes_central = [ node_vis_id ],
            node_label_off_num_nodes = 1000,
            figsize = (6, 6),
            fig_face_color = fig_face_color,
            title = "Network around %s" % node_vis_id,
            outfile = image_file)
        
    nodes_drawn = [ NichoNode.objects.get(node_vis_id = nodenam)
                    for nodenam in nodes_drawn ]
    print("Nodes drawn:", nodes_drawn)

    hwidth_zi = int(hwidth/1.5)
    if hwidth_zi < 2:
        hwidth_zi = 2
    hheight_zi = int(hheight/1.5)
    if hheight_zi < 2:
        hheight_zi = 2

    zoom_in_param = { "hwidth"  : hwidth_zi,
                      "hheight" : hheight_zi,
                      "offx"    : offx,
                      "offy"    : offy }
    
    zoom_out_param = { "hwidth"  : int(hwidth*1.5),
                       "hheight" : int(hheight*1.5),
                       "offx"    : offx,
                       "offy"    : offy }
    
    shift_left_param = { "hwidth"  : hwidth,
                         "hheight" : hheight,
                         "offx"    : int(offx - hwidth*0.5),
                         "offy"    : offy }

    shift_right_param = { "hwidth"  : hwidth,
                          "hheight" : hheight,
                          "offx"    : int(offx + hwidth*0.5),
                          "offy"    : offy }

    shift_down_param = { "hwidth"  : hwidth,
                         "hheight" : hheight,
                         "offx"    : offx,
                         "offy"    : int(offy - hheight*0.5) }


    shift_up_param = { "hwidth"  : hwidth,
                       "hheight" : hheight,
                       "offx"    : offx,
                       "offy"    : int(offy + hheight*0.5) }
    
     
    contxt = RequestContext(request, { "image_url"   : image_url,
                                       "nodes_drawn" : nodes_drawn,
                                       "zoom_in_param"     : zoom_in_param,                                       
                                       "zoom_out_param"    : zoom_out_param,
                                       "shift_left_param"  : shift_left_param,
                                       "shift_right_param" : shift_right_param,
                                       "shift_up_param"    : shift_up_param,
                                       "shift_down_param"  : shift_down_param,                                       
                                        })
    templt = loader.get_template("appNichoAnu/map_Anurag_del_node1.html")
    
    return HttpResponse(templt.render(contxt)) 
    

