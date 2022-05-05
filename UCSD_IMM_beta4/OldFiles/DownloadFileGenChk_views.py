
import os
import io

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from django.conf import settings

from Processes.MultiProcsTermAtExit_simple1 import terminate_inactive_processes


# http://127.0.0.1:8000/downloadfilegenchk/tmpout1_done.txt/

FILE_DOWNLOAD_DIR = os.path.join(settings.MEDIA_ROOT,
                                 "FilesToBeDownloaded", "Mess") 

def filecheck(request, chkfilename):
    
    contxt = RequestContext(request,
                            { "chkfilename" : chkfilename })
    templt = loader.get_template("DownloadFileGenChk/filechk1_3.html")
    
    return HttpResponse(templt.render(contxt))


# http://127.0.0.1:8000/downloadfilegenchk/srv/tmpfile1_done.txt/
# UCSD_IMM_beta4/UCSD_IMM_WorkSpace/FilesToBeDownloaded/Mess/tmpfile1_done.txt

def filecheck_server(request, chkfilename):
    
    filepath = os.path.join(FILE_DOWNLOAD_DIR, chkfilename)
    
    if os.path.isfile(filepath):
        ret_h = {"FileFound" : "True"}
    else:
        ret_h = {"FileFound" : "False"}
    
    return JsonResponse(ret_h)
    

def file_download(request, chkfilename):
    
    filepath = os.path.join(FILE_DOWNLOAD_DIR, chkfilename)
    
    # output = io.StringIO()
    # output.write("First line.\n")
    response = HttpResponse(open(filepath, "rb"), content_type="application/octet-stream")
    response["Content-Disposition"] = "filename=%s" % chkfilename
    
    terminate_inactive_processes()
    
    return response    
    
    # return HttpResponse(chkfilename + " ready.")

def timeout(request):
    
    contxt = RequestContext(request,
                            {  })
    templt = loader.get_template("DownloadFileGenChk/timeout1_1.html")
    
    return HttpResponse(templt.render(contxt))    
    


