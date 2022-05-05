from django.shortcuts import render

# Create your views here.

import os
import io

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from django.conf import settings

from Processes.MultiProcsTermAtExit_simple1_2 import terminate_inactive_processes, get_all_processes

from UCSD_IMM_Usefuls.UCSD_IMM_UniqStamp1_1 import get_existing_stamp_info 
from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG

FILEGEN_CHECK_DIR = os.path.join(settings.UCSD_IMM_INFOTRANSFDIR,
                                 "FileGenChk1") 

# Try http://127.0.0.1:8000/cycfilegenchk/main/testcheck1
# after placing testcheck1_json1.txt in UCSD_IMM_INFOTRANSFDIR
def filecheck(request, istamp_core):
    """ Javascript in the template (client-side) is expected to call filecheck_server,
    and eventually found_error, file_ok or timeout. """

    param_h = get_existing_stamp_info(istamp_core)
    
    chk_base_filename = param_h["chk_base_filename"]
    err_base_filename = param_h["err_base_filename"]
    
    contxt = RequestContext(request,
                            { "chk_base_filename"   : chk_base_filename,
                              "err_base_filename"   : err_base_filename,
                              "uniqstamp_core"      : istamp_core,
                              "proc_millisec"       :   5000,
                              "itimeintrv_millisec" :    250,
                              "timeout_millisec"    : 180000, })
    templt = loader.get_template("CycFileGenChk/filechk1_8.html")
    
    return HttpResponse(templt.render(contxt))

# Try http://127.0.0.1:8000/cycfilegenchk/srv/testcheck1/
# after placing testcheck1_json1.txt in UCSD_IMM_INFOTRANSFDIR
def filecheck_server(request, istamp_core):
    """ This function may be called from Javascript """
   
    param_h = get_existing_stamp_info(istamp_core)
    
    chk_base_filename = param_h["chk_base_filename"]
    err_base_filename = param_h["err_base_filename"]

    loGG()["func"]("[ At periodical check ] ...",
                    extra = loGG()["extra"])
    for procnum in get_all_processes():
        proc = get_all_processes()[ procnum ]
        loGG()["func"]("Recognized process at periodical check: %s"
                       % str(proc), extra = loGG()["extra"])
          
    ofilepath = os.path.join(FILEGEN_CHECK_DIR, chk_base_filename)
    efilepath = os.path.join(FILEGEN_CHECK_DIR, err_base_filename)
    
    if os.path.isfile(efilepath):
        # This should come first. As soon as the error file is generated, we have an error.
        ret_h = { "status" : "terminated by error" } 
    elif os.path.isfile(ofilepath):
        ret_h = { "status" : "normal termination" }
    else:
        ret_h = { "status" : "termination not detected" }
    
    # terminate_inactive_processes()
    # This may be unnecessary if terminate_all_processes() works at the end of Python process.
    return JsonResponse(ret_h)
    
    
def found_error(request, istamp_core):

    param_h = get_existing_stamp_info(istamp_core)
    
    err_base_filename = param_h["err_base_filename"]
    
    errstrlist = open(os.path.join(FILEGEN_CHECK_DIR,
                                   err_base_filename)).readlines()
    # errstr = errstr.replace('\n', "<BR/>\n") # <BR/> will be shown as it is.

    contxt = RequestContext(request,
                            { "errstrlist" : errstrlist })
    templt = loader.get_template("CycFileGenChk/error1_3.html")
    
    # terminate_inactive_processes()
    return HttpResponse(templt.render(contxt)) 


# http://127.0.0.1:8000/cycfilegenchk/ok/testcheck1/
# after placing testcheck1_json1.txt in UCSD_IMM_INFOTRANSFDIR
def file_ok(request, istamp_core):
    """ HTML in chk_base_filename will be used for output """

    param_h = get_existing_stamp_info(istamp_core)
    
    chk_base_filename = param_h["chk_base_filename"]
    
    okstr = "".join(open(os.path.join(FILEGEN_CHECK_DIR,
                                      chk_base_filename)).readlines())
    
    return HttpResponse(okstr)
    # Not sure if this works for DjangoSafeText.

def timeout(request, istamp_core):
    
    param_h = get_existing_stamp_info(istamp_core)    
        
    contxt = RequestContext(request,
                            {  })
    templt = loader.get_template("CycFileGenChk/timeout1_2.html")
    
    # Defunct process may be made.
    return HttpResponse(templt.render(contxt))    
    
