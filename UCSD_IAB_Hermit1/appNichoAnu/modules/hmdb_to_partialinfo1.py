
import os
import pandas as pd
from django.conf import settings
from rs_Python_Pack3_copied.General_Packages.FileDirPath.Pickle_Manager4_3 import Pickle_Manager
from rs_Python_Pack3_copied.General_Packages.FileDirPath.mkdir_on_absent import mkdir_on_absent
from rs_Python_Pack3_copied.General_Packages.FileDirPath.File_Path1 import rs_filepath_info

hmdb_tsv_file = os.path.join(settings.STATICFILES_DIRS[0],
                             "appNichoAnu", "PubData",
                             "hmdb3_3_dfrm1.tsv")

def generate_hmdb_partialinfo_dfrm(ihmdb_tsv_file):
    
    imed_hmdb_to_partialinfo_dfrm = \
        pd.io.parsers.read_table(ihmdb_tsv_file,
                                 sep = '\t', header = 0, index_col = 0,
                                 encoding = "latin1")
        
    imed_dfrm = \
        imed_hmdb_to_partialinfo_dfrm.loc[:, ("KEGG ID",
                                              "CAS number",
                                              "Wikipidia",
                                              "Name")]
    odfrm = imed_dfrm.applymap(lambda ielem: str(ielem).strip())
    
    return odfrm

pkl_file = os.path.join(settings.UCSD_IAB_WORKDIR,
                        "InterMed", "PubData",
                        "hmdb3_3_partial_dfrm.pkl")
mkdir_on_absent(rs_filepath_info(pkl_file)[ "foldername" ])
                             
pmI2 = Pickle_Manager(source_files = [ hmdb_tsv_file ],
                      version_info_h = { "Ver major": "0.54", },
                      pkl_file = pkl_file,
                      verbose = True,
                      ifunc = generate_hmdb_partialinfo_dfrm,
                      args = [ hmdb_tsv_file ],
                      kwargs = {})

hmdb_partial_info_dfrm = pmI2.get_obj()
