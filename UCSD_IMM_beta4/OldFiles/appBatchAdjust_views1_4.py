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
import time
from numpy import mean, median # Or try to replace ALL by from statistics import ...
import pandas as pd

# import multiprocessing
from Processes.MultiProcsTermAtExit_simple1_2 import invoke_process

from FileUpload.models import FileUploaded, Project, DataType
from CycFileGenChk.views import FILEGEN_CHECK_DIR

from FileDirPath.File_Path_Conv1 import file_path_conv_guess
from FileDirPath.File_Path1 import rs_filepath_info    
from FileDirPath.rsFilePath1 import RSFPath
from FileDirPath.mkdir_on_absent import mkdir_on_absent
from FileDirPath.UniqStamp_simple1 import UniqStamp_simple

from Usefuls.NumStr_commas import NumStr_rm_commas, NumStr_commas_to_decpoints


from Nephrology.MetabDatProc1.Rplot_batch_PDFout1_1 import invoke_Rplot_batch_PDFout
from Nephrology.MetabDatProc1.Metab_Batch_Adjust_SingleFile1_8 \
    import Metab_Batch_Adjust_SingleFile

from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG
# from UCSD_IMM_Usefuls.UCSD_IMM_InfoTransf_via_file2 import write_transf_info

# FILEGEN_CHECK_DIR = os.path.join(settings.UCSD_IMM_INFOTRANSFDIR,
#                                  "FileGenChk1") import it!

LAST_N = 3

BADJ_TSV_DIR    = os.path.join(settings.UCSD_IMM_WORKDIR,
                               "appBatchAdjust", "TSV")
BADJ_PDF_DIR    = os.path.join(settings.UCSD_IMM_WORKDIR,
                               "appBatchAdjust", "PDF")
COLNAM_BATCHNUM = "Batch No"
COLNAM_SAMPLEID = "Sample ID"
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
    
    
    uniqstamp = UniqStamp_simple()
    uniqstamp.set_stamped_files_dir(settings.UCSD_IMM_INFOTRANSFDIR)
    outbasefilnam = uniqstamp.stamp_on("%s_done.xlsx")
    errbasefilnam = uniqstamp.stamp_on("%s_errr.txt")
    
    mkdir_on_absent(BADJ_TSV_DIR)
    mkdir_on_absent(BADJ_PDF_DIR)

    oxlsx_file = os.path.join(FILEGEN_DOWNLOAD_DIR, outbasefilnam)

    otsvbfilnam = rs_filepath_info(input_fpath)["base_filename_wo_ext"] + "_badj1.tsv"
    otsv_fpath  = os.path.join(BADJ_TSV_DIR, otsvbfilnam)

    # For PDF file generation
    pdfout_fpath_wo_ext = \
        os.path.join(BADJ_PDF_DIR,
                     uniqstamp.stamp_on("TMP_%s")) # Without file extension

    pdfout_merged_fpath = \
        os.path.join(BADJ_PDF_DIR,
                     uniqstamp.stamp_on("appBA_%s"))
                
    uniqstamp.\
        write_json_stamped_file(
            { "chk_base_filename"   : outbasefilnam,
              "err_base_filename"   : errbasefilnam,
              "oxlsx_fpath"         : oxlsx_file,
              "otsv_fpath"          : otsv_fpath,
              "pdfout_fpath_wo_ext" : pdfout_fpath_wo_ext,
              "pdfout_merged_fpath" : pdfout_merged_fpath,
              })
    
    ctrlsampnameprefix   = request.POST["ctrlsampnameprefix"]
    smallvalforzerosnans = float(request.POST["smallvalforzerosnans"])
    commaasdpoint        = request.POST.get("commaasdpoint", False)
    mn_func_sel          = request.POST[ "mn_func_sel" ]

    loGG()["func"]("ctrlprefix:%s, smallvalzero:%f, commaflag:%s"
                   % (ctrlsampnameprefix, smallvalforzerosnans,
                      commaasdpoint), extra = loGG()["extra"])
    
    invoke_process(target = initiate,
                   args = (uniqstamp,
                           errbasefilnam,
                           input_fpath,
                           mn_func_sel,
                           ctrlsampnameprefix,
                           smallvalforzerosnans,
                           commaasdpoint))

    return HttpResponseRedirect(reverse("DownloadFileGenChk:filecheck",
                                        kwargs = { "istamp" : uniqstamp.get_stamp_core() }))


def initiate(istamp,
             err_base_filename,
             input_fpath,
             mn_func_sel,
             ctrlsampnameprefix,
             smallvalforzerosnans,
             commaasdpoint):
    
    try:
        # from time import sleep
        # sleep(5)
        # open("/file/that/does/not/exist")

        uniqstamp = UniqStamp_simple(istamp)
        uniqstamp.set_stamped_files_dir(settings.UCSD_IMM_INFOTRANSFDIR)  
        param_h = uniqstamp.read_json_stamped_file()
        chk_base_filename   = param_h["chk_base_filename"]
        # err_base_filename   = param_h["err_base_filename"]
        oxlsx_fpath         = param_h["oxlsx_fpath"]
        otsv_fpath          = param_h["otsv_fpath"]
        pdfout_fpath_wo_ext = param_h["pdfout_fpath_wo_ext"]
        pdfout_merged_fpath = param_h["pdfout_merged_fpath"]
            
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
    
        mn_func = { "mean"   : mean,
                    "median" : median }[ mn_func_sel ]

        loGG()["func"]("Selected function: %s by %s"
                       % (mn_func, mn_func_sel, ), extra = loGG()["extra"]) 

        mbas = Metab_Batch_Adjust_SingleFile(
            metab_dfrm             = imetab_dfrm,
            ctrl_colnam_key_prefix = ctrlsampnameprefix,
            calcfunc               = mn_func,
            smallval_for_zerosnans = smallvalforzerosnans,
            smallval_for_zerosnans_ctrl_only_mode = True,
            colname_batch_no = COLNAM_BATCHNUM,
            colname_sampleid = COLNAM_SAMPLEID)

        mbas.adjust_write(oxlsx_fpath, otsv_fpath)
            
        invoke_Rplot_batch_PDFout(imetab_bunc_batch_file = imetabfile,
                                  imetab_badj_batch_file = otsv_fpath,
                                  imn_func_switch_str = mn_func_sw,
                                  icolname_batch_no = COLNAM_BATCHNUM,
                                  icolname_sampleid = COLNAM_SAMPLEID,
                                  imctrl_prefix = ctrlsampnameprefix,
                                  pdf_save_fpath_wo_ext = pdfout_fpath_wo_ext,
                                  pdf_merged_save_fpath = pdfout_merged_fpath)        
            
    except Exception as inst:
        open(os.path.join(FILEGEN_DOWNLOAD_DIR, err_base_filename), "w").\
            write(str(inst))
        

