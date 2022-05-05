from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from django.conf import settings

from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG

@login_required
def entry(request):
    
    lun = request.user.username
    
    loGG(lun=lun)["func"]("Entering table of contents.",
                          extra = loGG(lun=lun)["extra"])
    
    contxt = RequestContext(request,
                            { "username": lun })
    
    templt = loader.get_template("UCSD_IMM_ToC/toc1.html")
    return HttpResponse(templt.render(contxt))


    