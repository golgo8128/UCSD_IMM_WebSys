
import os
import io

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from django.conf import settings

from Processes.MultiProcsTermAtExit_simple1_2 import terminate_inactive_processes, get_all_processes

from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG

FILEGEN_DOWNLOAD_DIR = os.path.join(settings.MEDIA_ROOT,
                                    "FilesToBeDownloaded", "Mess") 


def filecheck(request, chk_base_filename, err_base_filename):
    """ Javascript in the template (client-side) is expected to call filecheck_server,
    and eventually found_error, file_download(_pre) or timeout. """
    
    contxt = RequestContext(request,
                            { "chk_base_filename"   : chk_base_filename,
                              "err_base_filename"   : err_base_filename,
                              "proc_millisec"       :   5000,
                              "itimeintrv_millisec" :    250,
                              "timeout_millisec"    : 180000, })
    templt = loader.get_template("DownloadFileGenChk/filechk1_5.html")
    
    return HttpResponse(templt.render(contxt))


def filecheck_server(request, chk_base_filename, err_base_filename):
    """ This function may be called from Javascript """

    loGG()["func"]("[ At periodical check ] ...",
                    extra = loGG()["extra"])
    for procnum in get_all_processes():
        proc = get_all_processes()[ procnum ]
        loGG()["func"]("Recognized process at periodical check: %s"
                       % str(proc), extra = loGG()["extra"])
          
    ofilepath = os.path.join(FILEGEN_DOWNLOAD_DIR, chk_base_filename)
    efilepath = os.path.join(FILEGEN_DOWNLOAD_DIR, err_base_filename)
    
    if os.path.isfile(efilepath):
        ret_h = { "status" : "terminated by error" }
    elif os.path.isfile(ofilepath):
        ret_h = { "status" : "normal termination" }
    else:
        ret_h = { "status" : "termination not detected" }
    
    # terminate_inactive_processes()
    # This may be unnecessary if terminate_all_processes() works at the end of Python process.
    return JsonResponse(ret_h)
    
    
def found_error(request, err_base_filename):
    
    errstr = "".join(open(os.path.join(FILEGEN_DOWNLOAD_DIR,
                                       err_base_filename)).readlines())
    errstr = errstr.replace('\n', "<BR/>\n")

    contxt = RequestContext(request,
                            { "errstr" : errstr })
    templt = loader.get_template("DownloadFileGenChk/error1_1.html")
    
    # terminate_inactive_processes()
    return HttpResponse(templt.render(contxt)) 
    
def file_download_pre(request, chk_base_filename):
    """ Javascript in the template should call file_download """

    contxt = RequestContext(request,
                            { "chk_base_filename" : chk_base_filename })
    
    templt = loader.get_template("DownloadFileGenChk/download1_1.html")  
    return HttpResponse(templt.render(contxt)) 


def file_download(request, chk_base_filename):
    
    filepath = os.path.join(FILEGEN_DOWNLOAD_DIR, chk_base_filename)
    
    response = HttpResponse(open(filepath, "rb"),
                            content_type="application/octet-stream")
    response["Content-Disposition"] = "filename=%s" % chk_base_filename

    for procnum in get_all_processes():
        proc = get_all_processes()[ procnum ]
        loGG()["func"]("Recognized process at possible termination: %s"
                       % str(proc), extra = loGG()["extra"])  
    
    # terminate_inactive_processes()
    return response   


def timeout(request):
    
    contxt = RequestContext(request,
                            {  })
    templt = loader.get_template("DownloadFileGenChk/timeout1_1.html")
    
    # Defunct process may be made.
    return HttpResponse(templt.render(contxt))    
    


