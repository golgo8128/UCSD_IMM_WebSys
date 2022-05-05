#!/usr/bin/env python
'''
Created on 2016/04/18

@author: rsaito
'''

import os
from collections import defaultdict
from datetime import datetime, timedelta
import pickle


class TimeStamp_HashFile:
    def __init__(self,
                 hashfilename,
                 save_past_timedelta = timedelta(days = 100)):
        
        self.hashfilename = hashfilename
        self.save_past_timedelta = save_past_timedelta
        self.load_stamp()

    def load_stamp(self):
        
        if os.path.isfile(self.hashfilename):
            self.stamp_h = pickle.load(file = open(self.hashfilename, "rb"))
        else:
            self.stamp_h = defaultdict(list)
        
    def stamp(self, ikey):

        ctime = datetime.now()
        self.stamp_h[ikey].append(ctime)
        # time should be in order
        while (len(self.stamp_h[ikey]) and
               self.stamp_h[ikey][0] < ctime - self.save_past_timedelta):
            print("Deleting", ikey, self.stamp_h[ikey][0])
            self.stamp_h[ikey].pop(0)
            
        pickle.dump(obj  = self.stamp_h,
                    file = open(self.hashfilename, "wb"))
        
    def get_keys_timerange(self, itimedelta_from, itimedelta_to = None):
        
        key_h = set()
        ctime = datetime.now()
        
        for ikey in self.stamp_h:
            if itimedelta_to:
                for tstamp in self.stamp_h[ ikey ]:
                    if ctime - itimedelta_from <= tstamp and tstamp < ctime - itimedelta_to:
                        key_h |= set([ikey])
                        break
            else:
                if self.stamp_h[ ikey ][-1] >= ctime - itimedelta_from:
                    key_h |= set([ikey])
        
        return key_h           
        

if __name__ == '__main__':

    ts_hf = TimeStamp_HashFile(os.path.join(os.environ["RS_TMP_DIR"],
                                            "timestamp_hashfile1_1.pkl"),
                               timedelta(seconds = 30))
    # ts_hf.stamp("Key #1")
    ts_hf.stamp("Key #2")
    # ts_hf.stamp("Key #3")
    # ts_hf.stamp("Key #4")
    # ts_hf.stamp("Key #5")
    from pprint import pprint
    pprint(ts_hf.stamp_h)
    # print(ts_hf.count_keys(timedelta(days = 7)))
    
    print(ts_hf.get_keys_timerange(timedelta(seconds = 20),
                                   timedelta(seconds = 15)))
    print(datetime.now())
    