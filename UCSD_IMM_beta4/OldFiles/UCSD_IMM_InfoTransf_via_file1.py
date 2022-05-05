#!/usr/bin/env python

import os
import json
from django.conf import settings
from FileDirPath.mkdir_on_absent import mkdir_on_absent
from UCSD_IMM_Usefuls.UCSD_IMM_uniq_stamp1 import gen_uniq_stamp_based_on_time

INFO_TRANSF_DIR = os.path.join(settings.UCSD_IMM_WORKDIR,
                               "InfoTransf")
INFO_TRANSF_FORMAT = "%s_json.txt"

def stamp_to_json_rwfile(istamp):
    
    return os.path.join(INFO_TRANSF_DIR,
                        INFO_TRANSF_FORMAT % istamp)

def write_transf_info(idic, stamp = None):
    
    mkdir_on_absent(INFO_TRANSF_DIR)
    
    if not stamp or "%s" in stamp:
        stamp = gen_uniq_stamp_based_on_time(stamp)

    json.dump(idic, open(stamp_to_json_rwfile(stamp), "w"))
    
    return stamp


def load_transf_info(istamp):
    
    return(json.load(open(stamp_to_json_rwfile(istamp))))

    
    