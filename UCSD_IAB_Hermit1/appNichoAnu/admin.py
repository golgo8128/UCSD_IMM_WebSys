from django.contrib import admin

# Register your models here.

from .models import NichoNode, NichoEdge, \
    NichoEdge_classification, NichoEdge_categorizationI, \
    NichoNode_obsolete, NichoEdge_obsolete
    
admin.site.register([ NichoNode,
                      NichoEdge,
                      NichoEdge_classification,
                      NichoEdge_categorizationI,
                      NichoNode_obsolete,
                      NichoEdge_obsolete ])