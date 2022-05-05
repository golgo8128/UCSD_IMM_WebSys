#!/usr/bin/env python

# Intended to be executed (imported) from ./manage.py shell
# then do "from appNichoAnu.utilities.data_import1_2 import *"
# or
# echo "from appNichoAnu.utilities.data_import1_2 import *" | ./manage.py shell

import pandas as pd
from datetime import datetime
from collections import OrderedDict

from FileDirPath.rsFilePath1 import RSFPath
from Usefuls.InstancesAttrs_trans_DFrm1_5 import InstancesAttrs_trans_DFrm
from Usefuls.datetime_format1 import str_to_rsTimeTZ, rsTimeTZ_to_str 

from django.contrib.auth.models import User
from appNichoAnu.models import *

# object.id may not be preserved.

node_file = RSFPath("TRUNK",
                    "cWorks", "Students",
                    "IkarashiM", "MetabMap_Nicholson",
                    "node_Anu_out1_4.tsv")

edge_file = RSFPath("TRUNK",
                    "cWorks", "Students",
                    "IkarashiM", "MetabMap_Nicholson",
                    "edge_Anu_out1_4.tsv")

def str_wo_space(ivar):
    return str(ivar).replace(" ", "_")

iatd_node = InstancesAttrs_trans_DFrm(
    NichoNode,
    OrderedDict((
        ("user", lambda itmpuser: User.objects.get(username = itmpuser)),
        ("timestamp", (str_to_rsTimeTZ, rsTimeTZ_to_str)),
        ("node_id", str),
        ("node_vis_id", str_wo_space), # for visualization
        ("hmdb_id", str), 
        ("kegg_id", str),
        ("cas_id", str),
        ("chebi_id", str),
        ("classification", str),
        ("annotation", str),
        ("source_dbname", str),
        ("reliability", int),    
        ("pos_x_on_map", float),
        ("pos_y_on_map", float),
        ("note", str),)),
    import_post_assign_func = lambda iinsttmp: iinsttmp.save())
        # ("obsolete", bool))))

NichoEdge.objects.all().delete() # !!!! BE CAREFUL !!!!
NichoNode.objects.all().delete() # !!!! BE CAREFUL !!!!
NichoEdge_obsolete.objects.all().delete()
NichoNode_obsolete.objects.all().delete()


import_node_dfrm = pd.io.parsers.read_table(node_file,
                                            sep = '\t', header = 0, index_col = 0)
node_insts_h = iatd_node.import_from_strDFrm(import_node_dfrm)


def tmp_get_node_vis_id(itmp_node_vis_id):
    
    try:
        nodeobj = NichoNode.objects.get(node_vis_id = itmp_node_vis_id.replace(" ", "_"))
    except:
        print(itmp_node_vis_id)
        raise
        
    return nodeobj

def i0f(objs):

    if objs.exists():
        return objs[0]
    else:
        return None


iatd_edge = InstancesAttrs_trans_DFrm(
    NichoEdge,
    OrderedDict((    
        ("user", lambda itmp_user: User.objects.get(username = itmp_user)),
        ("timestamp", (str_to_rsTimeTZ, rsTimeTZ_to_str)),
        ("edge_id", str),
        ("node_src", tmp_get_node_vis_id),
         # lambda itmp_node_vis_id: NichoNode.objects.get(node_vis_id = itmp_node_vis_id)),
        ("node_tgt", tmp_get_node_vis_id),
         # lambda itmp_node_vis_id: NichoNode.objects.get(node_vis_id = itmp_node_vis_id)),
        ("is_directed", bool),
        ("ecnums", str),
        ("coupled_reaction_note", str),
        ("classification",
         lambda itmp_classif: i0f(NichoEdge_classification.objects.filter(class_name = itmp_classif))),
        ("categorization_I",
         lambda itmp_categI: i0f(NichoEdge_categorizationI.objects.filter(categ_name = itmp_categI))),
        ("annotation",  str),
        ("pubdb_name", str),
        ("pubdb_id", str), 
        ("reliability", int),
        ("note", str))),
    import_post_assign_func = lambda iinsttmp: iinsttmp.save())


import_edge_dfrm = pd.io.parsers.read_table(edge_file,
                                            sep = '\t', header = 0, index_col = 0)
edge_insts_h = iatd_edge.import_from_strDFrm(import_edge_dfrm)

