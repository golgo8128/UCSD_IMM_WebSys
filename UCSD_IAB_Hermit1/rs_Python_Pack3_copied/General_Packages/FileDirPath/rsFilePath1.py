#!/usr/bin/env python
'''
Created on 2015/12/26

@author: rsaito
'''

import os

RS_ENV_DIR_FORMAT = "RS_%s_DIR"

def RSFPath(rs_envar, *addpath):
    
    return os.path.join(os.environ[RS_ENV_DIR_FORMAT % rs_envar],
                        *addpath)
    
def RSFPath_conv(istr):
    # Do from rsFilePath import RSFPath
    
    if istr.startswith("RSFPath(") and istr.endswith(")"):
        return eval(istr)
    else:
        return istr

def RSFPath_convs(istr_list):
    
    return [ RSFPath_conv(istr) for istr in istr_list ]


if __name__ == '__main__':

    print(RSFPath("DESKTOP", "tmpdir", "tmp1.txt"))
    print(RSFPath_conv('RSFPath("DESKTOP", "tmpdir")'))
    print(RSFPath_convs([ 'RSFPath("DESKTOP", "tmpdir1")',
                          "/test/dir",
                          'RSFPath("DESKTOP", "tmpdir2")',
                          'RSFPath("TMP", "tmpdir3")' ]))
    

    