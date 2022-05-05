from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

import os
import json
import multiprocessing
import time

from FileUpload.models import FileUploaded, Project, DataType

LAST_N = 3

@login_required
def entry(request):
    
    fupobjs = \
        FileUploaded.objects.filter(idatatype =
            DataType.objects.get(datatype =
                "Metab levels in each batch")).order_by("-itimestamp")[:LAST_N]

    contxt = RequestContext(request,
                            { "fupobjs" : fupobjs })
    templt = loader.get_template("appBatchAdjust/proc_singlefile1_tmplt1.html")
    
    return HttpResponse(templt.render(contxt))
    # RemovedInDjango110Warning: render() must be called with a dict, not a RequestContext.
 
#    return render(request, "appBatchAdjust/proc_singlefile1_tmplt1.html", contxt)
   
#    templt = loader.get_template("appBatchAdjust/proc_singlefile1_tmplt1.html")    
#    return HttpResponse(templt.render({ "fupobjs" : fupobjs }))
    
#     contxt = RequestContext(request,
#                             { "fupobjs" : fupobjs })
#     templt = loader.get_template("appBatchAdjust/proc_singlefile1_tmplt1.html")
#     return HttpResponse(templt.render(contxt))

@login_required
def invoke(request):
    
    input_fpath = \
        FileUploaded.objects.get(id = request.POST["selfilobj"]).ifile.path
    
    outbasefilnam = "tmpout11_%s_done.txt" % hex(int(time.time() * 100000))[2:]
    # Try for i in range(100): print(hex(int(time.time() * 100000))) on server.
    
    proc = multiprocessing.Process(target = initiate,
                                   args = (outbasefilnam,
                                           input_fpath))
    proc.start()

    return HttpResponseRedirect(reverse("DownloadFileGenChk:filecheck",
                                        kwargs = { "chkfilename" : outbasefilnam }))

def initiate(outbasefilnam, input_fpath):

    from time import sleep
    sleep(10)    

    filepath = os.path.join(settings.UCSD_IMM_WORKDIR,
                            "FilesToBeDownloaded", "Mess", outbasefilnam) 
    open(filepath, "w").write("""Hello.
This is a test.
--- %s ---
- %s -
Good bye!
""" % (outbasefilnam, input_fpath))

# http://stackoverflow.com/questions/28837217/django-create-a-changing-button-or-waiting-page
# http://stackoverflow.com/questions/8512143/how-to-create-a-waiting-page-in-django
# http://stackoverflow.com/questions/9822763/displaying-a-temporary-page-while-processing-a-get-request

# http://api.jquery.com/jquery.getjson/
# http://akiniwa.hatenablog.jp/entry/2013/10/06/124757
# http://chase-seibert.github.io/blog/2012/01/27/using-access-control-allow-origin-to-make-cross-domain-post-requests-from-javsacript.html


# ... probably this does not work? Cookies may not be sent in XMLHttpRequest
# --> but, actually, it works!?
# --> No, XMLHttpRequest cannot deal with login prompt.
# http://127.0.0.1:8000/app/BatchAdjust/testjson/Worked
# @login_required 
def test_json_ret1(request, param1):
    
    return JsonResponse({"Data1": param1,
                         "Data2": "Hi"})
    # https://benjaminhorn.io/code/setting-cors-cross-origin-resource-sharing-on-apache-with-correct-response-headers-allowing-everything-through/

#     response = HttpResponse(json.dumps({"Data1": param1,
#                                         "Data2": "Hi"}), content_type="application/json")
#     response["Access-Control-Allow-Origin"] = "*"
#     response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT" # More methods available?
#     response["Access-Control-Max-Age"] = "1000"
#     response["Access-Control-Allow-Headers"] = "*"
#    return response


