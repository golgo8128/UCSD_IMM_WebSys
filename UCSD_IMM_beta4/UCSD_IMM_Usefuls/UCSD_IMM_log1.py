#!/usr/bin/env python

import os
import platform
import getpass
import logging

from django.conf import settings

LOGVER = "0.81"

# Probably this function is most useful among all in this module.
def loGG(ilevel = "info", lun = "a_user"):
    
    if getpass.getuser() == settings.APACHE_USERNAME:
        logger_logins = logging.getLogger("prodserv_log")
    else:
        logger_logins = logging.getLogger("testserv_log")
    
    logger_method = getattr(logger_logins, ilevel)
    
    return {"func": logger_method,
            "extra" : {"hostname"  : platform.uname()[1],
                       "username"  : getpass.getuser(),
                       "logver"    : LOGVER,
                       "loginuser" : lun }}

def output_log(message, ilevel = "info"):

    if getpass.getuser() == settings.APACHE_USERNAME:
        logger_logins = logging.getLogger("prodserv_log")
    else:
        logger_logins = logging.getLogger("testserv_log")
    
    logger_method = getattr(logger_logins, ilevel)
    logger_method(message, extra = {"hostname": os.uname()[1],
                                    "username": getpass.getuser() })
    

def get_output_log_func(ilevel = "info"):

    if getpass.getuser() == settings.APACHE_USERNAME:
        logger_logins = logging.getLogger("prodserv_log")
    else:
        logger_logins = logging.getLogger("testserv_log")
    
    logger_method = getattr(logger_logins, ilevel)
    
    return (lambda imessage:
                logger_method(imessage, extra = {"hostname": os.uname()[1],
                                                 "username": getpass.getuser() }))
    
    
class Output_Log:
    def __init__(self, ilevel = "info"):
        self.ilevel = ilevel
        
    def record_log(self, message):
        if getpass.getuser() == settings.APACHE_USERNAME:
            logger_logins = logging.getLogger("prodserv_log")
        else:
            logger_logins = logging.getLogger("testserv_log")
            logger_method = getattr(logger_logins, self.ilevel)
            logger_method(message, extra = {"hostname": os.uname()[1],
                                            "username": getpass.getuser() })
        
        
        
    
