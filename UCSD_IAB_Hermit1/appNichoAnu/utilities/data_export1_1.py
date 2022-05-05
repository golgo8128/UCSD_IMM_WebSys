#!/usr/bin/env python

# Intended to be executed (imported) from ./manage.py shell
# then do "from appNichoAnu.utilities.data_export1_1 import *"
# or
# echo "from appNichoAnu.utilities.data_export1_1 import *" | ./manage.py shell

import pandas as pd
from collections import OrderedDict
from FileDirPath.rsFilePath1 import RSFPath
from Usefuls.InstancesAttrs_trans_DFrm1_3 import InstancesAttrs_trans_DFrm

from django.contrib.auth.models import User
from appNichoAnu.models import *

# object.id may not be preserved.

node_file = RSFPath("DESKTOP",
                    "node_Anu_out1_3_1.tsv")

edge_file = RSFPath("DESKTOP",
                    "edge_Anu_out1_3_1.tsv")

iatd_node = InstancesAttrs_trans_DFrm(
    NichoNode,
    OrderedDict((
        ("user", lambda itmpuser: User.objects.get(username = itmpuser)),
        ("timestamp", (str_to_rsTimeTZ, rsTimeTZ_to_str)),
        ("node_id", str),
        ("node_vis_id", str), # for visualization
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
        ("note", str),)))
        # ("obsolete", bool))))

node_insts_h = OrderedDict(
    [(nodeobj.id, nodeobj)
     for nodeobj in NichoNode.objects.all()])

exported_node_dfrm = iatd_node.export_to_strDFrm(node_insts_h)
exported_node_dfrm.to_csv(node_file,
                          sep = '\t', header = True, index = True)

iatd_edge = InstancesAttrs_trans_DFrm(
    NichoEdge,
    OrderedDict((    
        ("user", lambda itmp_user: User.objects.get(username = itmp_user)),
        ("timestamp", (str_to_rsTimeTZ, rsTimeTZ_to_str)),
        ("edge_id", str),
        ("node_src",
         lambda itmp_node_vis_id: NichoNode.objects.get(node_vis_id = itmp_node_vis_id)),
        ("node_tgt",
         lambda itmp_node_vis_id: NichoNode.objects.get(node_vis_id = itmp_node_vis_id)),
        ("is_directed", bool),
        ("ecnums", str),
        ("coupled_reaction_note", str),
        ("classification",
         lambda itmp_classif: NichoEdge_classification.objects.get(class_name = itmp_classif)),
        ("categorization_I",
         lambda itmp_categI: NichoEdge_categorizationI.objects.get(class_name = itmp_categI)),
        ("annotation",  str),
        ("pubdb_name", str),
        ("pubdb_id", str), 
        ("reliability", int),
        ("note", str))))

edge_insts_h = OrderedDict(
    [(edgeobj.id, edgeobj)
     for edgeobj in NichoEdge.objects.all()])

exported_edge_dfrm = iatd_edge.export_to_strDFrm(edge_insts_h)
exported_edge_dfrm.to_csv(edge_file,
                          sep = '\t', header = True, index = True)

