#!/usr/bin/env python


import dateutil.parser
import pytz

import django
from django.conf import settings

try:
    TIME_ZONE_THISSERVER = settings.TIME_ZONE_THISSERVER
except django.core.exceptions.ImproperlyConfigured:
    TIME_ZONE_THISSERVER = "US/Pacific"

# pytz.timezone("US/Pacific").localize(dateutil.parser.parse("2016/03/01 23:15"))

def get_tzone_str():
    
    return TIME_ZONE_THISSERVER

class TMPTimeKlass:
    def __init__(self,
                 tzone = pytz.timezone(get_tzone_str())):
        
        self.tzone = tzone
        
        self.start_datetime     = None
        self.end_datetime       = None
        
        self.start_datetime_str = ""
        self.end_datetime_str   = ""
               
        self.start_date_str     = ""
        self.start_time_hh_str  = "09"
        self.start_time_mm_str  = "00"       

        self.end_date_str       = ""
        self.end_time_hh_str    = "17"
        self.end_time_mm_str    = "00"  
        
        self.internal_copy()
        
    def import_post_req(self, request_post,
                        keyw_start = "start",
                        keyw_end   = "end"):

        self.start_date_str    = request_post.get("%s_date"    % keyw_start, "")
        self.start_time_hh_str = request_post.get("%s_time_hh" % keyw_start, "09")
        self.start_time_mm_str = request_post.get("%s_time_mm" % keyw_start, "00")
        
        self.end_date_str      = request_post.get("%s_date"    % keyw_end, "")
        self.end_time_hh_str   = request_post.get("%s_time_hh" % keyw_end, "17")
        self.end_time_mm_str   = request_post.get("%s_time_mm" % keyw_end, "00")
        
        self.parse_start_end_datetime()
        self.internal_copy()
        
    def parse_start_end_datetime(self):

        if len(self.start_date_str):
            self.start_datetime_str = "%s %s:%s" % (self.start_date_str,
                                                    self.start_time_hh_str,
                                                    self.start_time_mm_str)
            self.start_datetime = \
                self.tzone.localize(dateutil.parser.parse(self.start_datetime_str))        
        else:
            self.start_datetime = None
        

        if len(self.end_date_str):
            self.end_datetime_str = "%s %s:%s" % (self.end_date_str,
                                                  self.end_time_hh_str,
                                                  self.end_time_mm_str)
            self.end_datetime = \
                self.tzone.localize(dateutil.parser.parse(self.end_datetime_str))
        else:
            self.end_datetime = None          

    def internal_copy(self):
        
        self.begin_datetime      = self.start_datetime
        self.finish_datetime     = self.end_datetime
        
        self.begin_datetime_str  = self.start_datetime_str
        self.finish_datetime_str = self.end_datetime_str
               
        self.begin_date_str      = self.start_date_str 
        self.begin_time_hh_str   = self.start_time_hh_str
        self.begin_time_mm_str   = self.start_time_mm_str       

        self.finish_date_str     = self.end_date_str 
        self.finish_time_hh_str  = self.end_time_hh_str
        self.finish_time_mm_str  = self.end_time_mm_str  
        

if __name__ == "__main__":
    
    tmptime1 = TMPTimeKlass()
    tmptime1.import_post_req({ "start_date" : "2001/3/12",
                               "end_date"   : "2001/3/15" })
    print(tmptime1.begin_datetime)
    print(tmptime1.end_datetime)
       