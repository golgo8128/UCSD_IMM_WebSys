from django.db import models

# Create your models here.

from django.contrib.auth.models import User # , AnonymousUser
from django.db.models import Q
from django.forms import ModelForm
from django import forms
from django.utils import timezone

from .modules.hmdb_to_partialinfo1 import hmdb_partial_info_dfrm

class NichoNode(models.Model):
    """ Ex. citric acid can have two nichonodes with same node_id
    but different node_vis_ids, which are intended for two citric acids
    in different pathway map locations """ 
    
    user         = models.ForeignKey(User, verbose_name = "User",
                                     on_delete = models.CASCADE)
    timestamp    = models.DateTimeField("Modified time")
        
    node_id      = models.CharField(verbose_name = "Node ID", max_length = 25)
    node_vis_id  = models.CharField(primary_key = True,
                                    default = "", max_length = 25,
                                    verbose_name = "Node ID for visual.")
    # for visualization

    hmdb_id      = models.CharField(default = "", max_length = 25,
                                    verbose_name = "HMDB ID", blank = True)
    kegg_id      = models.CharField(default = "", max_length = 25,
                                    verbose_name = "KEGG ID", blank = True)
    cas_id       = models.CharField(default = "", max_length = 25,
                                    verbose_name = "CAS Number", blank = True)
    chebi_id     = models.CharField(default = "", max_length = 25,
                                    verbose_name = "CHEBI ID", blank = True)    

    classification = models.CharField(default = "", max_length = 100,
                                      verbose_name = "Classification",
                                      blank = True) 
    
    annotation   = models.CharField(default = "", max_length = 200,
                                    verbose_name = "Annotation") 
    
    source_dbname = models.CharField(default = "", max_length = 30,
                                     verbose_name = "Source DB Name",
                                     blank = True) 
    
    reliability  = models.IntegerField(default = 2, null = True, blank = True)
    
    pos_x_on_map = models.FloatField(verbose_name = "X-coordinate on the map")
    pos_y_on_map = models.FloatField(verbose_name = "Y-coordinate on the map")
    
    label_offset100_x = models.FloatField(verbose_name = "Label offset X (%)",
                                          default = 0, blank = True)
    label_offset100_y = models.FloatField(verbose_name = "Label offset Y (%)",
                                          default = 0, blank = True)
    
    note         = models.TextField(default = "", blank = True)

    def number_of_nodes(self):
        return len(self.__class__.objects.all())

    def incoming_edges(self):
        
        return NichoEdge.objects.filter(node_tgt = self)
    
    def outgoing_edges(self):

        return NichoEdge.objects.filter(node_src = self) 

    def assoc_edges(self):
        
        return NichoEdge.objects.filter(Q(node_src = self) |
                                        Q(node_tgt = self))


    def conv_hmdb_to_name(self):
        
        if (len(self.hmdb_id) and
            self.hmdb_id in hmdb_partial_info_dfrm.index
            and len(str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "Name"]))):
            return str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "Name"])
        else:
            return "-"

    def conv_hmdb_to_kegg(self):
                
        if (len(self.hmdb_id) and
            self.hmdb_id in hmdb_partial_info_dfrm.index
            and len(str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "KEGG ID"]))):
            return str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "KEGG ID"])
        else:
            return None

    def conv_hmdb_to_cas(self):
        
        if (len(self.hmdb_id) and
            self.hmdb_id in hmdb_partial_info_dfrm.index
            and len(str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "CAS number"]))):
            return str(hmdb_partial_info_dfrm.loc[self.hmdb_id, "CAS number"])
        else:
            return None

    
    def get_spec_node_citric_acid(self):
        
        return self.__class__.objects.get(hmdb_id="HMDB00094")
    
    def generate_obsolete(self, itimestamp = None):
        # Unsaved to database.
        
        node_obso = NichoNode_obsolete()
        node_obso.node_vis_id_obsolete = self.node_vis_id
        
        if itimestamp:
            node_obso.timestamp_obso = itimestamp
        else:
            node_obso.timestamp_obso = timezone.now()

        for fieldname in (
            "user",
            "timestamp",
            "node_id",
            # "node_vis_id",
            "hmdb_id",
            "kegg_id",
            "cas_id",
            "chebi_id",
            "classification",
            "annotation",
            "source_dbname",
            "reliability",
            "pos_x_on_map",
            "pos_y_on_map",
            "label_offset100_x",
            "label_offset100_y",
            "note"
            ):
            setattr(node_obso,
                    fieldname,
                    getattr(self, fieldname)) 
        
        return node_obso # Unsaved here.
        

    class Meta:
        verbose_name        = "Node"
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.node_vis_id
       

class NichoNode_Form(ModelForm):
    
    annotation = forms.CharField(widget=forms.TextInput(attrs = { "size" : 60 }))
    note       = forms.CharField(widget=forms.Textarea(attrs = { "rows" : 10,
                                                                 "cols" : 75 }))
    
    del_node   = forms.BooleanField(required = False)
    
    class Meta:
        model = NichoNode
        exclude = ("user", "timestamp")


class NichoEdge_classification(models.Model):
    
    class_name = models.CharField(max_length = 100,
                                  verbose_name = "Class Name") 
    note       = models.TextField(default = "") 
    
    class Meta:
        verbose_name        = "Edge classification"
        verbose_name_plural = "Edge classifications"
    
    def __str__(self):

        return self.class_name
    

class NichoEdge_categorizationI(models.Model):
    
    categ_name = models.CharField(max_length = 100,
                                  verbose_name = "Category I Name") 
    note       = models.TextField(default = "") 
    
    class Meta:
        verbose_name        = "Edge categorization I"
        verbose_name_plural = "Edge categorizations I"   
        
    def __str__(self):

        return self.categ_name


class NichoEdge(models.Model):
    
    user        = models.ForeignKey(User, verbose_name = "User",
                                    on_delete = models.CASCADE,)
    timestamp   = models.DateTimeField("Modified time")
    edge_id     = models.CharField(max_length = 200, null = True, blank = True)
    node_src    = models.ForeignKey(NichoNode,
                                    on_delete = models.CASCADE,
                                    related_name = "node_src",
                                    verbose_name = "Source node")
    node_tgt    = models.ForeignKey(NichoNode,
                                    on_delete = models.CASCADE,
                                    related_name = "node_tgt",
                                    verbose_name = "Target node")
    is_directed = models.BooleanField(verbose_name = "Is directed?")
    ecnums      = models.CharField(default = "",
                                   max_length = 300, verbose_name = "EC numbers",
                                   blank = True)
    # Two nichoedges are necessary for two EC numbers corresponding to
    # the same reaction.
    
    coupled_reaction_note = models.CharField(default = "", max_length = 500,
                                             verbose_name = "Coupled reaction note",
                                             blank = True)
    
    classification = models.ForeignKey(NichoEdge_classification,
                                       on_delete = models.SET_NULL,
                                       null = True, blank = True,
                                       verbose_name = "Classification") 
    categorization_I = models.ForeignKey(NichoEdge_categorizationI,
                                         on_delete=models.SET_NULL,
                                         null = True, blank = True,
                                         verbose_name = "Categorization I") 
 
    
    annotation = models.CharField(default = "", max_length = 300,
                                  verbose_name = "Annotation",
                                  blank = True)     
    
    # Just one public DB entry
    pubdb_name = models.CharField(default = "", max_length = 25,
                                  null = True, blank = True)
    pubdb_id   = models.CharField(default = "", max_length = 25,
                                  null = True, blank = True)
    
    relay_pos_x1_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y1_on_map = models.FloatField(null = True, blank = True)    
    relay_pos_x2_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y2_on_map = models.FloatField(null = True, blank = True) 
    relay_pos_x3_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y3_on_map = models.FloatField(null = True, blank = True)     
    
    reliability = models.IntegerField(default = 2, null = True, blank = True)
    note        = models.TextField(default = "", blank = True)   

    def judge_edge_same_orient_bool(self, iedge):
        """ Three possible return values:
        True, False, None.
        Be careful to discriminate False and None
        """
        
        if (iedge.node_src == self.node_src and
            iedge.node_tgt == self.node_tgt):
            return True
        elif (iedge.node_tgt == self.node_src and
              iedge.node_src == self.node_tgt):
            return False
        else:
            return None

    def get_same_pair_edges(self, inc_reverse = False): # This includes self
        
        if inc_reverse:
            return NichoEdge.objects.filter(
                Q(node_src = self.node_src,
                  node_tgt = self.node_tgt) | 
                Q(node_src = self.node_tgt,
                  node_tgt = self.node_src)).order_by("-timestamp")            
        else:
            return NichoEdge.objects.filter(node_src = self.node_src,
                                            node_tgt = self.node_tgt).order_by("-timestamp")
        
    def get_relay_set(self):
        
        ret = []
        if (self.relay_pos_x1_on_map is not None and 
            self.relay_pos_y1_on_map is not None):
            ret.append((self.relay_pos_x1_on_map,
                        self.relay_pos_y1_on_map))
        if (self.relay_pos_x2_on_map is not None and 
            self.relay_pos_y2_on_map is not None):
            ret.append((self.relay_pos_x2_on_map,
                        self.relay_pos_y2_on_map))
        if (self.relay_pos_x3_on_map is not None and 
            self.relay_pos_y3_on_map is not None):
            ret.append((self.relay_pos_x3_on_map,
                        self.relay_pos_y3_on_map))
        
        return ret
        
    def pick_one_relay_set(self,
                           self_bool = False, inc_reverse = False):

        if self_bool:
            return self.get_relay_set()
        else:
            for edge in self.get_same_pair_edges(inc_reverse):
                relay_set = edge.get_relay_set()
                if self.judge_edge_same_orient_bool(edge) is False:
                    relay_set = relay_set[::-1]
                if len(relay_set):
                    return relay_set
            return []

    def number_of_edges(self):
        return len(self.__class__.objects.all())

    def get_ecnums_strs(self):
        
        return [ ecnum.strip()
                 for ecnum in self.ecnums.split(',') 
                 if len(ecnum.strip()) ]

    def get_categI_str(self):
        if self.categorization_I:
            return str(self.categorization_I)
        else:
            return "-"

    def get_edgelabelI_str(self):
        
        if len(self.get_ecnums_strs()):
            return "|".join(self.get_ecnums_strs())
        elif self.categorization_I:
            return str(self.categorization_I)
        else:
            return "-"


    def generate_obsolete(self, itimestamp = None):
        # Unsaved to database.
        
        edge_obso = NichoEdge_obsolete()
        edge_obso.node_src_vis_id_obsolete = self.node_src.node_vis_id
        edge_obso.node_tgt_vis_id_obsolete = self.node_tgt.node_vis_id
        
        if itimestamp:
            edge_obso.timestamp_obso = itimestamp
        else:
            edge_obso.timestamp_obso = timezone.now()

        for fieldname in (
            "user",
            "timestamp",
            "edge_id",
            # "node_src",
            # "node_tgt"
            "is_directed",
            "ecnums",
            "coupled_reaction_note",
            "classification",
            "categorization_I",
            "annotation",
            "pubdb_name",
            "pubdb_id",
            "relay_pos_x1_on_map",
            "relay_pos_y1_on_map",
            "relay_pos_x2_on_map",
            "relay_pos_y2_on_map",
            "relay_pos_x3_on_map",
            "relay_pos_y3_on_map",
            "reliability",
            "note"
            ):
            setattr(edge_obso,
                    fieldname,
                    getattr(self, fieldname)) 
        
        return edge_obso # Unsaved here.


    class Meta:
        verbose_name        = "Edge"
        verbose_name_plural = "Edges"


    def __str__(self):

        return "%s %s %s" % (self.node_src.node_vis_id,
                             { True  : "->",
                               False : "--" }[ self.is_directed ],
                             self.node_tgt.node_vis_id)


class NichoEdge_Form(ModelForm):
    
    annotation = forms.CharField(widget=forms.TextInput(attrs ={ "size" : 75 }),
                                 required = False) 
    coupled_reaction_note = forms.CharField(widget=forms.TextInput(attrs ={ "size" : 75 }),
                                            required = False)    
    note = forms.CharField(widget=forms.Textarea(attrs = { "rows" : 10,
                                                           "cols" : 75 }),
                           required = False)    
    
    del_edge = forms.BooleanField(required = False)
    """
<input id="id_del_edge" name="del_edge" type="checkbox"
  onclick="clicked_del_edge(this, 'label_del_edge');" />
<label for="id_del_edge" id="label_del_edge">Delete this edge</label>
"""
    
    class Meta:
        model = NichoEdge
        exclude = ("user", "timestamp")
        

# To make modifications completely reversible (trackable),
# each modification step must be reversible.
class NichoNode_obsolete(models.Model):
    """ Ex. citric acid can have two nichonodes with same node_id
    but different node_vis_ids, which are intended for two citric acids
    in different pathway map locations """ 
    
    user           = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
                                       verbose_name = "User")
    timestamp      = models.DateTimeField("Modified time")
    timestamp_obso = models.DateTimeField("Became obsolete on") 
        
    node_id      = models.CharField(verbose_name = "Node ID", max_length = 25)

    # Not a primary key any more
    node_vis_id_obsolete = models.CharField(default = "", max_length = 25,
                                            verbose_name = "Node ID for visual.")

    
    # for visualization

    hmdb_id      = models.CharField(default = "", max_length = 25,
                                    verbose_name = "HMDB ID", blank = True)
    kegg_id      = models.CharField(default = "", max_length = 25,
                                    verbose_name = "KEGG ID", blank = True)
    cas_id       = models.CharField(default = "", max_length = 25,
                                    verbose_name = "CAS Number", blank = True)
    chebi_id     = models.CharField(default = "", max_length = 25,
                                    verbose_name = "CHEBI ID", blank = True)    

    classification = models.CharField(default = "", max_length = 100,
                                      verbose_name = "Classification",
                                      blank = True) 
    
    annotation   = models.CharField(default = "", max_length = 200,
                                    verbose_name = "Annotation") 
    
    source_dbname = models.CharField(default = "", max_length = 30,
                                     verbose_name = "Source DB Name",
                                     blank = True) 
    
    reliability  = models.IntegerField(default = 2, null = True, blank = True)
    
    pos_x_on_map = models.FloatField(null = True, blank = True)
    pos_y_on_map = models.FloatField(null = True, blank = True)
    
    label_offset100_x = models.FloatField(verbose_name = "Label offset X (%)",
                                          default = 0, blank = True)
    label_offset100_y = models.FloatField(verbose_name = "Label offset Y (%)",
                                          default = 0, blank = True)    
    
    note         = models.TextField(default = "", blank = True)
    
    modification_log = models.TextField(default = "")
   
    class Meta:
        verbose_name        = "Obsolete node"
        verbose_name_plural = "Obsolete nodes"

    def __str__(self):
        return "%s (obsolete on %s)" % (self.node_vis_id_obsolete,
                                        str(self.timestamp_obso))


class NichoEdge_obsolete(models.Model):
    
    user           = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
                                       verbose_name = "User")
    timestamp      = models.DateTimeField("Modified time")
    timestamp_obso = models.DateTimeField("Became obsolete on") 
    edge_id     = models.CharField(max_length = 200, null = True, blank = True)
    node_src_vis_id_obsolete  = models.CharField(default = "", max_length = 25,
                                                 verbose_name = "Source node obsolete")
    node_tgt_vis_id_obsolete  = models.CharField(default = "", max_length = 25,
                                                 verbose_name = "Target node obsolete")
    is_directed = models.BooleanField(verbose_name = "Is directed?")
    ecnums      = models.CharField(default = "",
                                   max_length = 300, verbose_name = "EC numbers",
                                   blank = True)
    # Two nichoedges are necessary for two EC numbers corresponding to
    # the same reaction.
    
    coupled_reaction_note = models.CharField(default = "", max_length = 500,
                                             verbose_name = "Coupled reaction note",
                                             blank = True)
    
    classification = models.ForeignKey(NichoEdge_classification,
                                       on_delete=models.SET_NULL,
                                       null = True, blank = True,
                                       verbose_name = "Classification") 
    categorization_I = models.ForeignKey(NichoEdge_categorizationI,
                                         on_delete=models.SET_NULL,
                                         null = True, blank = True,
                                         verbose_name = "Categorization I") 
 
    
    annotation = models.CharField(default = "", max_length = 300,
                                  verbose_name = "Annotation",
                                  blank = True)     
        
    # Just one public DB entry
    pubdb_name = models.CharField(default = "", max_length = 25,
                                  null = True, blank = True)
    pubdb_id   = models.CharField(default = "", max_length = 25,
                                  null = True, blank = True)
    
    relay_pos_x1_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y1_on_map = models.FloatField(null = True, blank = True)    
    relay_pos_x2_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y2_on_map = models.FloatField(null = True, blank = True) 
    relay_pos_x3_on_map = models.FloatField(null = True, blank = True)
    relay_pos_y3_on_map = models.FloatField(null = True, blank = True)    
    
    reliability = models.IntegerField(default = 2, null = True, blank = True)
    note        = models.TextField(default = "", blank = True)   

    modification_log = models.TextField(default = "")

    class Meta:
        verbose_name        = "Obsolete edge"
        verbose_name_plural = "Obsolete edges"


    def __str__(self):

        return "%s %s %s (obsolete on %s)" % (
                             self.node_src_vis_id_obsolete,
                             { True  : "->",
                               False : "--" }[ self.is_directed ],
                             self.node_tgt_vis_id_obsolete,
                             str(self.timestamp_obso))
    
    