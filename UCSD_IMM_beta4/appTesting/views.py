from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.conf import settings



def index(request):
    
    contxt = RequestContext(request,
                            { })
    
    templt = loader.get_template("appTesting/test_media_url1.html")
    return HttpResponse(templt.render(contxt))
