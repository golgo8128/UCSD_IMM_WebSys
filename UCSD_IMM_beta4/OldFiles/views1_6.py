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
from urllib.parse import urljoin

# import multiprocessing
from Processes.MultiProcsTermAtExit_simple1_2 import invoke_process

from FileUpload.models import FileUploaded, Project, DataType
from CycFileGenChk.views import FILEGEN_CHECK_DIR

from FileDirPath.File_URL_PathConv1_2 import File_URL_PathConv, file_path_conv_guess
from FileDirPath.File_Path1 import rs_filepath_info    
from FileDirPath.rsFilePath1 import RSFPath
from FileDirPath.mkdir_on_absent import mkdir_on_absent

from Usefuls.NumStr_commas import NumStr_rm_commas, NumStr_commas_to_decpoints


from Nephrology.MetabDatProc1.Rplot_batch_PDFout1_1 import invoke_Rplot_batch_PDFout
from Nephrology.MetabDatProc1.Metab_Batch_Adjust_SingleFile1_10 \
    import Metab_Batch_Adjust_SingleFile

from UCSD_IMM_Usefuls.UCSD_IMM_UniqStamp1_1 \
    import generate_new_stamp, get_existing_stamp_info 
from UCSD_IMM_Usefuls.UCSD_IMM_log1 import loGG


LAST_N = 3

(BADJ_TSV_DIRURL,
 BADJ_PDF_DIRURL,
 BADJ_XLS_DIRURL) = [
    File_URL_PathConv(userroot_dir = settings.MEDIA_ROOT,
                      userroot_url = settings.MEDIA_URL,
                      subpath = os.path.join("appBatchAdjust", iext))
    for iext in ("TSV", "PDF", "XLS")
 ]
                     

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
    # Guessing for multiple platform usages.
    # Don't have multiple folders with name "Media" in the paths.

    input_file_subpath = input_fpath.replace(settings.MEDIA_ROOT, "").lstrip('\\/')
    input_DIRURL = File_URL_PathConv(userroot_dir = settings.MEDIA_ROOT,
                                     userroot_url = settings.MEDIA_URL)
    
    loGG()["func"]("input_path_raw:%s, settings.MEDIA_ROOT:%s conv:%s"
                   % (input_path_raw, settings.MEDIA_ROOT, input_fpath), extra = loGG()["extra"])     
    
    uniqstamp = generate_new_stamp()

    outbasefilnam = uniqstamp.stamp_on("%s_done.html")
    errbasefilnam = uniqstamp.stamp_on("%s_errr.txt")
    
    mkdir_on_absent(BADJ_TSV_DIRURL.get_user_filepath())
    mkdir_on_absent(BADJ_PDF_DIRURL.get_user_filepath())
    mkdir_on_absent(BADJ_XLS_DIRURL.get_user_filepath())

    oxls_bfilnam = uniqstamp.stamp_on("%s_badj1.xlsx")
    otsv_bfilnam = uniqstamp.stamp_on("%s_badj1.tsv")
    itsv_bfilnam = uniqstamp.stamp_on("%s_input1.tsv")
    opdf_bfilnam = uniqstamp.stamp_on("appBA1_%s.pdf")

    oxls_fpath   = os.path.join(BADJ_XLS_DIRURL.get_user_filepath(),
                                oxls_bfilnam)
    otsv_fpath   = os.path.join(BADJ_TSV_DIRURL.get_user_filepath(),
                                otsv_bfilnam)
    itsv_fpath   = os.path.join(BADJ_TSV_DIRURL.get_user_filepath(),
                                itsv_bfilnam)

    # For PDF file generation
    pdfout_fpath_wo_ext = \
        os.path.join(BADJ_PDF_DIRURL.get_user_filepath(),
                     uniqstamp.stamp_on("TMP_%s")) # Without file extension

    pdfout_merged_fpath = \
        os.path.join(BADJ_PDF_DIRURL.get_user_filepath(),
                     opdf_bfilnam)
                    
    ctrlsampnameprefix   = request.POST["ctrlsampnameprefix"]
    smallvalforzerosnans = float(request.POST["smallvalforzerosnans"]) # Can we turn this off?
    commaasdpoint        = request.POST.get("commaasdpoint", False)
    mn_func_sel          = request.POST[ "mn_func_sel" ]

    loGG()["func"]("ctrlprefix:%s, smallvalzero:%f, commaflag:%s"
                   % (ctrlsampnameprefix, smallvalforzerosnans,
                      commaasdpoint), extra = loGG()["extra"])

    contxt = RequestContext(request,
                            { "PDFfile"  : BADJ_PDF_DIRURL.get_user_urlpath(opdf_bfilnam),
                              "XLSfile"  : BADJ_XLS_DIRURL.get_user_urlpath(oxls_bfilnam),
                              "iTSVfile" : BADJ_TSV_DIRURL.get_user_urlpath(itsv_bfilnam),
                              "oTSVfile" : BADJ_TSV_DIRURL.get_user_urlpath(otsv_bfilnam),
                              "irawfile" : input_DIRURL.get_user_urlpath(input_file_subpath),
                              })
    templt = loader.get_template("appBatchAdjust/badj_dl_links1_1.html")
    
    uniqstamp.\
        write_json_stamped_file(
            { "chk_base_filename"   : outbasefilnam,
              "err_base_filename"   : errbasefilnam,
              "oxls_fpath"          : oxls_fpath,
              "otsv_fpath"          : otsv_fpath,
              "itsv_fpath"          : itsv_fpath,
              "pdfout_fpath_wo_ext" : pdfout_fpath_wo_ext,
              "pdfout_merged_fpath" : pdfout_merged_fpath,
              "chk_file_html_cntnt" : templt.render(contxt),
              })
    
    invoke_process(target = initiate,
                   args = (uniqstamp,
                           errbasefilnam,
                           input_fpath,
                           mn_func_sel,
                           ctrlsampnameprefix,
                           smallvalforzerosnans,
                           commaasdpoint))

    return HttpResponseRedirect(reverse("CycFileGenChk:filecheck",
                                        kwargs = { "istamp_core" : uniqstamp.get_stamp_core() }))


def initiate(istamp,
             err_base_filename, # If attempt to read from param_h, 
                                # error may arise before executing the main code.
             input_fpath,
             mn_func_sel,
             ctrlsampnameprefix,
             smallvalforzerosnans,
             commaasdpoint):
    
    try:
        # from time import sleep
        # sleep(5)
        # open("/file/that/does/not/exist")

        param_h = get_existing_stamp_info(istamp)
        chk_base_filename   = param_h["chk_base_filename"]
        # err_base_filename   = param_h["err_base_filename"]
        oxls_fpath          = param_h["oxls_fpath"]
        otsv_fpath          = param_h["otsv_fpath"]
        itsv_fpath          = param_h["itsv_fpath"]
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
            calcmnfunc             = mn_func,
            smallval_for_zerosnans = smallvalforzerosnans,
            smallval_for_zerosnans_ctrl_only_mode = True,
            colname_batch_no = COLNAM_BATCHNUM,
            colname_sampleid = COLNAM_SAMPLEID)

        mbas.adjust_write(oxls_fpath, otsv_fpath, itsv_fpath)
            
        invoke_Rplot_batch_PDFout(imetab_bunc_batch_file = itsv_fpath, # imetabfile,
                                  imetab_badj_batch_file = otsv_fpath,
                                  imn_func_switch_str = mn_func_sel,
                                  icolname_batch_no = COLNAM_BATCHNUM,
                                  icolname_sampleid = COLNAM_SAMPLEID,
                                  imctrl_prefix = ctrlsampnameprefix,
                                  pdf_save_fpath_wo_ext = pdfout_fpath_wo_ext,
                                  pdf_merged_save_fpath = pdfout_merged_fpath)
        
        open(os.path.join(FILEGEN_CHECK_DIR, chk_base_filename),
             "w").write(param_h["chk_file_html_cntnt"])
            
    except Exception as inst: # ZeroDivisionError as inst: #  
        open(os.path.join(FILEGEN_CHECK_DIR, err_base_filename), "w").\
            write(str(inst))
        

