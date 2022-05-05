#!/usr/bin/env python
'''
Created on 2014/02/02

@author: rsaito
'''

import os

def rs_filepath_info(ipath):
    
    folder_name = os.path.dirname(ipath)
    bfile_name  = os.path.basename(ipath)
    
    if "." in bfile_name:
        bfile_name_wo_ext = ".".join(bfile_name.split(".")[:-1])
    else:
        bfile_name_wo_ext = bfile_name

    
    if len(bfile_name.split(".")) == 1:
        fext = ""
    else:
        fext = bfile_name.split(".")[-1]

    return { "ifilepath"     : ipath ,
             "foldername"    : folder_name, 
             "base_filename" : bfile_name,
             "file_ext"      : fext,
             "base_filename_wo_ext" : bfile_name_wo_ext, 
             "ifilepath_wo_ext"     : os.path.join(folder_name, bfile_name_wo_ext) }

def add_str_before_ext(ipath, istr):
    
    pathinfo = rs_filepath_info(ipath)
    if pathinfo["file_ext"] == "":
        return pathinfo["ifilepath_wo_ext"] + istr
    else:
        return pathinfo["ifilepath_wo_ext"] + istr + '.' + pathinfo["file_ext"]


if __name__ == "__main__":
    print(rs_filepath_info("/abc/def/ghijk.txt"))
    print(rs_filepath_info("/abc/def/ghijk"))    
    print(rs_filepath_info("/abc/def/"))  
    print(add_str_before_ext("/a/b/c/ddd.txt", "Hooooo"))
    print(add_str_before_ext("/a/b/c/ddd", "_Hooooo"))
    