#!/usr/bin/env python
'''
Created on 2014/08/15

@author: rsaito
'''

import os

def mkdir_on_absent(idir):
    
    if not os.path.exists(idir):
        os.makedirs(idir)
        
if __name__ == "__main__":
    mkdir_on_absent("/tmp/tmp193/tmp194")
    mkdir_on_absent("/tmp/tmp193/tmp194")
    