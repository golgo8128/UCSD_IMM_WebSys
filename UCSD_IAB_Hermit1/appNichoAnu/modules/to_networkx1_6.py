#!/usr/bin/env python

# Intended to be executed (imported) from ./manage.py shell
# then do:
#   from appNichoAnu.modules.to_networkx1_5 import *
#   grf = to_networkx_from_rec()
#   grf.output(keyw = True, noval_str = "---")
#   from Graph_Packages.Graph_Draw.DrawNetworkX_simple1_7 import *
#   drawgrf = DrawNetworkX_simple(grf)
#   drawgrf.output_fig_around_node("HMDB00094", outer = 5.0, rate = 0.0,
#                                  figsize = (18, 17),
#                                  outfile = "/Users/rsaito/Desktop/tmpintrxgraph1_3.pdf")

import os
from collections import defaultdict
import pickle # http://docs.python.jp/3/library/pickle.html

from django.conf import settings

# import networkx as nx
from rs_Python_Pack3_copied.Graph_Packages.NetworkX.rsNetworkX_DiGraph1 import rsNetworkX_DiGraph
from rs_Python_Pack3_copied.Graph_Packages.Graph_Draw.DrawNetworkX_simple1_9 \
    import KEY_NODE_COORD_XY, \
        KEY_DISP_NODE_LABEL, KEY_NODE_LABEL_OFFSET_XY, \
        KEY_EDGE_LABEL_LIST, KEY_EDGE_DIRECTION, KEY_EDGE_RELAY_POSS
from appNichoAnu.models import *

from rs_Python_Pack3_copied.General_Packages.FileDirPath.mkdir_on_absent import mkdir_on_absent
from rs_Python_Pack3_copied.General_Packages.FileDirPath.File_Path1 import rs_filepath_info

networkx_pkl_file = os.path.join(settings.UCSD_IAB_WORKDIR,
                             "Media", "appNichoAnu", "Network",
                             "NichoAnu_networkx_intermed1_2.pkl")
mkdir_on_absent(rs_filepath_info(networkx_pkl_file)[ "foldername" ])


def del_networkx_rec():
    
    if os.path.isfile(networkx_pkl_file):
        os.remove(networkx_pkl_file)
    

def to_networkx_from_rec(update = False,
                         focus_edge = None):
    
    if not os.path.isfile(networkx_pkl_file) or update:
        ogrf = to_networkx()
        with open(networkx_pkl_file, "wb") as fw:
            pickle.dump(ogrf, fw)
    else:
        with open(networkx_pkl_file, "rb") as fh:
            ogrf = pickle.load(fh)
    
    if focus_edge:
        relay_poss = focus_edge.pick_one_relay_set(self_bool = True)
        # edge.get_relay_set()
        
        if ogrf.has_edge(str(focus_edge.node_src),
                         str(focus_edge.node_tgt)):
            ogrf.edges[ str(focus_edge.node_src),
                        str(focus_edge.node_tgt) ][ KEY_EDGE_RELAY_POSS ] = relay_poss

        elif ogrf.has_edge(str(focus_edge.node_tgt),
                           str(focus_edge.node_src)):
            ogrf.edges[ str(focus_edge.node_tgt),
                        str(focus_edge.node_src) ][ KEY_EDGE_RELAY_POSS ] = relay_poss[::-1]
        
        else:
            raise KeyError("%s not found" % str(focus_edge))
        
        
    return ogrf


def to_networkx():

    grf1 = rsNetworkX_DiGraph()
    edge_pair_to_ecnums_h = defaultdict(set)
    
    
    for edge in NichoEdge.objects.all():
        node_src    = edge.node_src
        node_tgt    = edge.node_tgt
        is_directed = edge.is_directed
        ecnums      = edge.ecnums

        relay_poss = edge.pick_one_relay_set(inc_reverse = True)
        
        if grf1.has_edge(str(node_tgt), str(node_src)):
            node_src, node_tgt = node_tgt, node_src
            relay_poss = relay_poss[::-1]
            dir_fwd = False
            if is_directed:
                dir_rev = True
            else:
                dir_rev = False
        else:
            grf1.add_edge(str(node_src), str(node_tgt))
            dir_rev = False
            if is_directed:
                dir_fwd = True
            else:
                dir_fwd = False
    
        if dir_fwd:
            grf1.edges[str(node_src), str(node_tgt)][ "dir_fwd" ] = dir_fwd
            # nx.set_edge_attributes(grf1,
            #     { (str(node_src), str(node_tgt)) : { "dir_fwd" : dir_fwd } })
        if dir_rev:
            grf1.edges[str(node_src), str(node_tgt)][ "dir_rev" ] = dir_rev
            # nx.set_edge_attributes(grf1,
            #     { (str(node_src), str(node_tgt)) : { "dir_rev" : dir_rev } })

        # grf1.edge[str(node_src)][str(node_tgt)]["dir_rev"] = dir_rev
        
        grf1.edges[ str(node_src), str(node_tgt) ][ KEY_EDGE_RELAY_POSS ] = relay_poss

        
        # print(edge.id, edge.timestamp,
        #       node_src, node_tgt, grf1.edge[ str(node_src) ][ str(node_tgt) ][ KEY_EDGE_RELAY_POSS ])
        
        if len(edge.get_ecnums_strs()):
            if "ecnum_set" not in grf1.edges[str(node_src), str(node_tgt)]:
                grf1.edges[str(node_src), str(node_tgt)][ "ecnum_set" ] = set()
            grf1.edges[str(node_src), str(node_tgt)][ "ecnum_set" ] |= set(edge.get_ecnums_strs())
                
                    
    for node_src_str, node_tgt_str in grf1.edges():
        if "ecnum_set" in grf1.edges[ node_src_str, node_tgt_str ]:
            grf1.edges[ node_src_str, node_tgt_str ][ KEY_EDGE_LABEL_LIST ] \
                = sorted(list(grf1.edges[ node_src_str, node_tgt_str ][ "ecnum_set" ]))
        
        dir_str_left = ""
        if grf1.edges[ node_src_str, node_tgt_str ].get("dir_rev", False):
            dir_str_left = "<"
        dir_str_right = ""
        if grf1.edges[ node_src_str, node_tgt_str ].get("dir_fwd", False):
            dir_str_right = ">"    
        dir_str = dir_str_left + "-" + dir_str_right
        grf1.edges[ node_src_str, node_tgt_str ][ KEY_EDGE_DIRECTION ] = dir_str

 
#     dg.add_edge("Node A", "Node C",
#                 **{ KEY_EDGE_LABEL_LIST : ["1.2.15.6", "3.1.1.4"],
#                     KEY_EDGE_RELAY_POSS : [(-3, 10), (-5, 6), (-9, 5)] })
        
    
    for node in NichoNode.objects.all():
        if not grf1.has_node(str(node)):
            grf1.add_node(str(node))
        grf1.nodes[str(node)][ KEY_DISP_NODE_LABEL ] = node.annotation
        grf1.nodes[str(node)][ KEY_NODE_COORD_XY ] = node.pos_x_on_map, node.pos_y_on_map
        grf1.nodes[str(node)][ KEY_NODE_LABEL_OFFSET_XY ] \
            = node.label_offset100_x, node.label_offset100_y
        
    return grf1


# grf = to_networkx()
# grf.output(keyw = True, noval_str = "---")

        
