#!/usr/bin/env python

import os
import json
from django.conf import settings
from FileDirPath.mkdir_on_absent import mkdir_on_absent
from Usefuls.UniqStamp_simple1 import UniqStamp_simple

INFO_TRANSF_DIR = os.path.join(settings.UCSD_IMM_WORKDIR,
                               "InfoTransf")
INFO_TRANSF_FORMAT = "%s_json.txt"

def stamp_to_json_rwfile(iuniqstamp):
    
    return iuniqstamp.stamp_on(os.path.join(INFO_TRANSF_DIR,
                                            INFO_TRANSF_FORMAT))

def write_transf_info(idic, iuniqstamp = None):
    
    mkdir_on_absent(INFO_TRANSF_DIR)
    
    if not iuniqstamp:
        iuniqstamp = UniqStamp_simple()

    json.dump(idic, open(stamp_to_json_rwfile(iuniqstamp), "w"))
    
    return stamp


def load_transf_info(iuniqstamp):
    
    return(json.load(open(stamp_to_json_rwfile(iuniqstamp))))

    
    