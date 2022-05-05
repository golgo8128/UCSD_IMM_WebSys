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
# import multiprocessing
from Processes.MultiProcsTermAtExit_simple1_2 import invoke_process
import time

from FileUpload.models import FileUploaded, Project, DataType
from DownloadFileGenChk.views1_2 import FILEGEN_DOWNLOAD_DIR

import os
import pandas as pd
from FileDirPath.File_Path_Conv1 import file_path_conv_guess
from Nephrology.MetabDatProc1.Metab_Batch_Adjust_SingleFile1_5 \
    import Metab_Batch_Adjust_SingleFile
from Usefuls.NumStr_commas import NumStr_rm_commas, NumStr_commas_to_decpoints

from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG
from UCSD_IMM_Usefuls.UCSD_IMM_uniq_stamp1 import gen_uniq_stamp_based_on_time
from UCSD_IMM_Usefuls.UCSD_IMM_InfoTransf_via_file1 import write_transf_info

LAST_N = 3

MetabDataStart_Colnum = 2

@login_required
def entry(request):
    
    fupobjs = \
        FileUploaded.objects.filter(idatatype =
            DataType.objects.get(datatype =
                "Metab levels in each batch")).order_by("-itimestamp")[:LAST_N]

    contxt = RequestContext(request,
                            { "fupobjs" : fupobjs })
    templt = loader.get_template("appBatchAdjust/proc_singlefile1_5.html")
    
    return HttpResponse(templt.render(contxt))
    # RemovedInDjango110Warning: render() must be called with a dict, not a RequestContext.
     

@login_required
def invoke(request):
    
    input_path_raw = \
        FileUploaded.objects.get(id = request.POST["selfilobj"]).ifile.name      
    input_fpath = file_path_conv_guess(input_path_raw, settings.MEDIA_ROOT)
    loGG()["func"]("input_path_raw:%s, settings.MEDIA_ROOT:%s conv:%s"
                   % (input_path_raw, settings.MEDIA_ROOT, input_fpath), extra = loGG()["extra"])     
    
    
    stamp = gen_uniq_stamp_based_on_time()
    outbasefilnam = "tmpout11_%s_done.xlsx" % stamp
    errbasefilnam = "tmpout11_%s_errr.txt"  % stamp
    
    write_transf_info({"Hello" : "Konnichiwa",
                       "Hi"    : "Yaa"}, stamp)
    
    ctrlsampnameprefix   = request.POST["ctrlsampnameprefix"]
    smallvalforzerosnans = float(request.POST["smallvalforzerosnans"])
    commaasdpoint        = request.POST.get("commaasdpoint", False)

    loGG()["func"]("ctrlprefix:%s, smallvalzero:%f, commaflag:%s"
                   % (ctrlsampnameprefix, smallvalforzerosnans,
                      commaasdpoint), extra = loGG()["extra"])
    
    invoke_process(target = initiate,
                   args = (outbasefilnam, errbasefilnam, 
                           input_fpath,
                           ctrlsampnameprefix, smallvalforzerosnans,
                           commaasdpoint))

    return HttpResponseRedirect(reverse("DownloadFileGenChk:filecheck",
                                        kwargs = { "chk_base_filename" : outbasefilnam,
                                                   "err_base_filename" : errbasefilnam }))


def initiate(outbasefilnam, errbasefilnam, input_fpath,
             ctrlsampnameprefix, smallvalforzerosnans,
             commaasdpoint):

    try:
        # from time import sleep
        # sleep(5)
        # open("/file/that/does/not/exist")
        
        imetabfile = input_fpath
        
        imetab_dfrm = pd.io.parsers.read_table(imetabfile,
                                               sep='\t',
                                               header = 0)
    
        if commaasdpoint:
            imetab_dfrm.iloc[:,MetabDataStart_Colnum:len(imetab_dfrm.columns)] = \
                imetab_dfrm.iloc[:,MetabDataStart_Colnum:len(imetab_dfrm.columns)].\
                    applymap(NumStr_commas_to_decpoints)
        else:
            imetab_dfrm.iloc[:,MetabDataStart_Colnum:len(imetab_dfrm.columns)] = \
                imetab_dfrm.iloc[:,MetabDataStart_Colnum:len(imetab_dfrm.columns)].\
                    applymap(NumStr_rm_commas)
    
        
        oxlsx_file = os.path.join(FILEGEN_DOWNLOAD_DIR, outbasefilnam)
        mbas = Metab_Batch_Adjust_SingleFile(imetab_dfrm,
                                             ctrlsampnameprefix,
                                             smallvalforzerosnans)
        mbas.adjust_write_excel(oxlsx_file)
        
    except Exception as inst:
        open(os.path.join(FILEGEN_DOWNLOAD_DIR, errbasefilnam), "w").\
            write(str(inst))
        

