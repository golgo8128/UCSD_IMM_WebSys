#!/usr/bin/env python

from django.conf import settings
from FileDirPath.UniqStamp_simple1 import UniqStamp_simple

def generate_new_stamp():

    uniqstamp = UniqStamp_simple()
    uniqstamp.set_stamped_files_dir(settings.UCSD_IMM_INFOTRANSFDIR)
    
    return uniqstamp

def get_existing_stamp(istamp):

    uniqstamp = UniqStamp_simple(istamp)
    uniqstamp.set_stamped_files_dir(settings.UCSD_IMM_INFOTRANSFDIR)
    
    return uniqstamp

def get_existing_stamp_info(istamp):
    
    uniqstamp = get_existing_stamp(istamp)
    return uniqstamp.read_json_stamped_file()

    