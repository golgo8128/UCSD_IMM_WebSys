#!/usr/bin/env python

# First, create a user Anurag.
# Intended to be executed (imported) from ./manage.py shell
# then do "from appNichoAnu.utilities.initial_dat_import1_3 import *"
# or
# echo "from appNichoAnu.utilities.initial_dat_import1_3 import *" | ./manage.py shell

import pandas as pd
import pytz
from datetime import datetime

from FileDirPath.rsFilePath1 import RSFPath

from django.contrib.auth.models import User
from django.db import IntegrityError
from ..models import *

node_file = RSFPath("TRUNK",
                    "cWorks", "Students",
                    "IkarashiM", "MetabMap_Nicholson",
                    "NicholsonMap_nodes_Anurag1_3_7.tsv")

edge_file = RSFPath("TRUNK",
                    "cWorks", "Students",
                    "IkarashiM", "MetabMap_Nicholson",
                    "NicholsonMap_edges_Anurag1_3_7.tsv")

node_coord_file = RSFPath("TRUNK",
                          "cWorks", "Students",
                          "IkarashiM", "MetabMap_Nicholson",
                          "NicholsonMap_nodescoord_Anurag1_1.tsv")

edge_validcheckres_file = RSFPath("TRUNK",
                                  "cWorks", "Students",
                                  "IkarashiM", "MetabMap_Nicholson",
                                  "NicholsonMap_edges_match_result1_3.tsv")

nodeinfo_coord_merge_ofile = RSFPath(
    "DESKTOP",
    "nichoanu_nodeinfo_coord_merged1_1.tsv")


node_dfrm = pd.io.parsers.read_table(node_file,
                                     header = 0, sep = "\t")
node_coord_dfrm = \
    pd.io.parsers.read_table(node_coord_file,
                             header = 0, sep = "\t").loc[:, ["IMM ID",
                                                             "position_x",
                                                             "position_y"]]

edge_dfrm = pd.io.parsers.read_table(edge_file,
                                     header = 0, sep = "\t")

edge_vcheck_dfrm = \
    pd.io.parsers.read_table(edge_validcheckres_file,
                             header = 0, sep = "\t").loc[:, ["IMM ID source",
                                                             "IMM ID target",
                                                             "Check items"]]

nodeinfo_coord_merge = pd.merge(node_dfrm, node_coord_dfrm,
                                on = ["IMM ID"], how = "left")

edgeinfo_vcheck_merge = pd.merge(edge_dfrm, edge_vcheck_dfrm,
                                 on = ["IMM ID source",
                                       "IMM ID target"], how = "left")


nodeinfo_coord_merge.to_csv(nodeinfo_coord_merge_ofile, sep = "\t")

# print(node_dfrm.iloc[0:10,:])
# print(node_coord_dfrm.iloc[0:10,:])
# print(nodeinfo_coord_merge.iloc[0:10,])
print(edgeinfo_vcheck_merge.iloc[0:20,])


NichoEdge.objects.all().delete() # !!!! BE CAREFUL !!!!
NichoNode.objects.all().delete() # !!!! BE CAREFUL !!!!
NichoEdge_classification.objects.all().delete() # !!!! BE CAREFUL !!!!
NichoEdge_categorizationI.objects.all().delete() # !!!! BE CAREFUL !!!!

NichoEdge_classification(class_name = "Biosynthesis").save()
NichoEdge_classification(class_name = "Degradation").save()
NichoEdge_classification(class_name = "Connection").save()

NichoEdge_categorizationI(categ_name = "Carbohydrates").save()
NichoEdge_categorizationI(categ_name = "Amino Acids").save()
NichoEdge_categorizationI(categ_name = "Lipids").save()
NichoEdge_categorizationI(categ_name = "Purines & Pyrimidines").save()
NichoEdge_categorizationI(categ_name = "Vitamins Co-enzymes & Hormones").save()
NichoEdge_categorizationI(categ_name = "Pentose Phosphate Pathway").save() #
NichoEdge_categorizationI(categ_name = "Photosynthesis Dark Reactions").save()
NichoEdge_categorizationI(categ_name = "Human Metabolism").save()

edge_color_to_categ_h = {
    "Green"  : "Carbohydrates",
    "Red"    : "Amino Acids",
    "Blue"   : "Lipids",
    "Purple" : "Purines & Pyrimidines",
    "Brown"  : "Vitamins Co-enzymes & Hormones",
    "Orange" : "Photosynthesis Dark Reactions",
    "Black"  : "Human Metabolism",
    }

simple_nonempty_check = (lambda istr: str(istr).lower() != "nan" and
                         len(str(istr).strip()))

for rownam in nodeinfo_coord_merge.index:
    new_nodeobj = NichoNode(user = User.objects.get(username = "Anurag"),
                            timestamp = pytz.timezone("US/Pacific").localize(datetime(2015, 12, 10, 10, 48)))
    new_nodeobj.node_id     = nodeinfo_coord_merge.loc[ rownam, "IMM ID"]
    new_nodeobj.node_vis_id = nodeinfo_coord_merge.loc[ rownam, "IMM ID"]
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "HMDB"]):
        new_nodeobj.hmdb_id = nodeinfo_coord_merge.loc[ rownam, "HMDB"]
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "CAS number"]):
        new_nodeobj.cas_id = nodeinfo_coord_merge.loc[ rownam, "CAS number"]
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "Metabolite name"]):
        new_nodeobj.annotation = nodeinfo_coord_merge.loc[ rownam, "Metabolite name"]
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "Source DB for manual ID assignment"]):
        new_nodeobj.source_dbname = nodeinfo_coord_merge.loc[ rownam, "Source DB for manual ID assignment"]
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "position_x"]):
        new_nodeobj.pos_x_on_map = int(float(nodeinfo_coord_merge.loc[ rownam, "position_x"])*100)/100.0
    if simple_nonempty_check(nodeinfo_coord_merge.loc[ rownam, "position_y"]):
        new_nodeobj.pos_y_on_map = int(float(nodeinfo_coord_merge.loc[ rownam, "position_y"])*100)/100.0

    try:
        new_nodeobj.save()
    except IntegrityError as err:
        print("##### Node information ntegrity error #####")
        print(nodeinfo_coord_merge.loc[ rownam, :])
        print()

for rownam in edgeinfo_vcheck_merge.index:

    note_h = {}
    
    new_edgeobj = NichoEdge(user = User.objects.get(username = "Anurag"),
                            timestamp = pytz.timezone("US/Pacific").localize(datetime(2015, 12, 13, 13, 4)))
    nodes_src = \
        NichoNode.objects.\
            filter(node_vis_id =
                   edgeinfo_vcheck_merge.loc[rownam, "IMM ID source"]) #,
                   # obsolete = False)
    if len(nodes_src) == 0:
        print(edgeinfo_vcheck_merge.loc[rownam, "IMM ID source"], "not found.")
        continue
    nodes_tgt = \
        NichoNode.objects.\
            filter(node_vis_id =
                   edgeinfo_vcheck_merge.loc[rownam, "IMM ID target"]) # ,
                   # obsolete = False)
    if len(nodes_tgt) == 0:
        print(edgeinfo_vcheck_merge.loc[rownam, "IMM ID target"], "not found.")
        continue
    
    new_edgeobj.node_src = nodes_src[0]
    new_edgeobj.node_tgt = nodes_tgt[0]
    
    if simple_nonempty_check(edgeinfo_vcheck_merge.loc[ rownam, "EC number"]):
        new_edgeobj.ecnums = edgeinfo_vcheck_merge.loc[ rownam, "EC number"]

    if simple_nonempty_check(edgeinfo_vcheck_merge.loc[ rownam, "Reaction type"]):
        react_type = edgeinfo_vcheck_merge.loc[ rownam, "Reaction type"]
        new_edgeobj.classification = NichoEdge_classification.objects.get(class_name = react_type)
    
    if simple_nonempty_check(edgeinfo_vcheck_merge.loc[ rownam, "Coupled reactions"]):
        new_edgeobj.coupled_reaction_note = edgeinfo_vcheck_merge.loc[ rownam, "Coupled reactions"]

    if simple_nonempty_check(edgeinfo_vcheck_merge.loc[ rownam, "Color of reaction"]):
        color_react = edgeinfo_vcheck_merge.loc[ rownam, "Color of reaction"]
        if color_react in edge_color_to_categ_h:
            new_edgeobj.categorization_I = NichoEdge_categorizationI.objects.get(categ_name = edge_color_to_categ_h[ color_react ])
    
    note_keywds = ("Color of reaction",
                   "NichoMap Coordinate Information",
                   "Note",
                   "Check items")
        
    for note_key in note_keywds:
        if simple_nonempty_check(edgeinfo_vcheck_merge.loc[ rownam, note_key]):
            note_h[ note_key ] = edgeinfo_vcheck_merge.loc[ rownam, note_key ]

    ostr = ""

    for note_key in note_keywds:
        if note_key in note_h:
            if len(ostr):
                if note_key == "Check items":
                    osep = "\n\n"
                else:
                    osep = ";  "
                ostr += osep
            if note_key == "Color of reaction":
                ostr += "%s: %s (%s)" % (note_key, note_h[ note_key ],
                                         edge_color_to_categ_h[note_h[ note_key ]])
            else:
                ostr += "%s: %s" % (note_key, note_h[ note_key ])


    new_edgeobj.note = ostr

    new_edgeobj.is_directed = True
    new_edgeobj.save()
    
    
