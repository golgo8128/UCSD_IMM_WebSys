#!/usr/bin/env python
'''
Created on 2013/11/15

@author: rsaito

Note: Use Python >=2.7
'''

"""
Tip for avoiding error of cPickling of classes having __getattr__
Python >= 2.7 required.

class TestClass2:
    def __init__(self, h):
        self.h = h
    def __getattr__(self, attrname):
        if attrname == "__setstate__":
            raise AttributeError("%r object has no attribute %s" %
                                 (self.__class__, attrname))
        else:
            return getattr(self.h, attrname)

http://blogs.yahoo.co.jp/golgo8128/40459902.html

"""


import os
import sys
import pickle
import pandas

from .simple_array_hash_file1 import simple_array_hash_file1
from .File_Path1 import rs_filepath_info
from .mkdir_on_absent import mkdir_on_absent
from .File_Path1 import add_str_before_ext
from .rsFilePath1 import RSFPath_convs

from rs_Python_Pack3_copied.Str_Proc.StrJoin_rs import strjoin_max



class Pickle_Manager:
    
    python_main_major_ver = 3
    PickMan_ver = "4.2.2"
    
    def __init__(self,
                 source_files,   # ex. ["sfile1", "sfile2", "sfile3"]
                 version_info_h, # This should be dictionary (ex. {"Version":"1.2", "Minor ver.":"0.3"}) or None.
                                 # All keys and values must be strings.
                 pkl_file,
                 verbose,
                 ifunc,   # Function to create object. from XXX import func function may not work.
                 args,    # args to be passed to the function
                 kwargs   # kwargs to be passed to the function
                 ):
        # Changes in parameters will not cause update of Pickle file.
        # If you do not want the program to read Pickle file which was created with
        # different parameters, parameters should be part of the Pickle file name (pkl_file) or
        # state as version info.

        if sys.version_info.major != self.python_main_major_ver:
            pkl_file = add_str_before_ext(pkl_file, "_Py%d" % sys.version_info.major)

        self.source_files   = source_files
        self.obj_file       = pkl_file
        self.version_info_h = version_info_h.copy()
        self.add_to_version_info()
        # self.version_info_h[ "PickMan version" ] = self.PickMan_ver # Adding item to mutable object

        self.non_str_val_check()

        pklfil_info_h = rs_filepath_info(self.obj_file)
        self.objinfo_file = pklfil_info_h[ "ifilepath_wo_ext" ] + "_objinfo1.txt"

        self.update = self.update_check()
        
        if self.update is True:
            if verbose:
                sys.stderr.write("To generate %s, reading original file(s) %s ...\n"
                                 % (self.obj_file,
                                    strjoin_max(RSFPath_convs(self.source_files), isep= ",")))
            self.src_files_exist_check()                
            self.obj = ifunc(*args, **kwargs)
            # See tip for avoiding error of cPickling of classes having __getattr__ on top.

            mkdir_on_absent(pklfil_info_h["foldername"])
            pklinfo_h = { "sfiles"   : self.source_files,
                          "versions" : self.version_info_h }
            simple_array_hash_file1(self.objinfo_file, pklinfo_h)
            self.save_obj_to_file()

        else:
            if self.update == "No source file check":
                if verbose:
                    sys.stderr.write("Without time-stamp check of source files, reading saved file %s [%s bytes] ...\n"
                                     % (self.obj_file, "{:,}".format(os.path.getsize(self.obj_file))))
            
            elif self.update:
                raise Exception("Unknown check-pass code", self.update)
            
            elif verbose:
                sys.stderr.write("Reading saved file %s [%s bytes] ...\n" % (self.obj_file, "{:,}".format(os.path.getsize(self.obj_file))))
            self.load_obj_from_file()
            

    def save_obj_to_file(self):
        
        fw = open(self.obj_file, "wb")
        pickle.dump(self.obj, fw)
        fw.close()


    def load_obj_from_file(self):

        fw = open(self.obj_file, "rb")
        self.obj = pickle.load(fw)
        fw.close()        

    def add_to_version_info(self):
        
        self.version_info_h[ "PickMan version" ] = self.PickMan_ver
        # Adding item to mutable object

    def get_update_flag(self):
        
        return self.update


    def update_check(self):

        if not os.path.isfile(self.obj_file):
            return True
        if not os.path.isfile(self.objinfo_file):
            return True
        
        pklinfo_prev_h = self.read_pklinfo_file()
        

        if pklinfo_prev_h[ "versions" ] != self.version_info_h: # dictionary comparison.
            return True
        
        if (len(pklinfo_prev_h.get("sfiles", [])) == 1 and
            pklinfo_prev_h["sfiles"][0] == "*"):
            return "No source file check"

        if (set(RSFPath_convs(pklinfo_prev_h.get("sfiles", [])))
            ^ set(RSFPath_convs(self.source_files))):
            return True

        self.src_files_exist_check()
        for src_file in RSFPath_convs(self.source_files):
            if (os.stat(src_file).st_mtime > os.stat(self.obj_file).st_mtime):
                return True
        
        return False

    def read_pklinfo_file(self):

        if os.path.isfile(self.objinfo_file):
            pklinfo_prev_h = simple_array_hash_file1(self.objinfo_file)
        else:
            pklinfo_prev_h = {"sfiles": [], "versions": {}}

        return pklinfo_prev_h

    def src_files_exist_check(self):
        
        for src_file in RSFPath_convs(self.source_files):
            if not os.path.isfile(src_file):
                raise FileNotFoundError('Source file "%s" not found.' % src_file)     


    def non_str_val_check(self):
        
        nonstr_keys = [ ikey for ikey in self.version_info_h.keys()   if type(ikey) is not str]
        nonstr_vals = [ ival for ival in self.version_info_h.values() if type(ival) is not str]

        if len(nonstr_keys):
            raise ValueError("Non-string keys for version info.: %s"   % str(nonstr_keys))
        if len(nonstr_vals):
            raise ValueError("Non-string values for version info.: %s" % str(nonstr_vals))             
        

    def get_obj(self):

        return self.obj


class PDDFRM_Manager(Pickle_Manager):
    """ Warning ... data may not be reproducible
    compared to Pickle_Manager.
    ex. blanks may turn into NaNs
    "123" may turn into 123. This may also happen for index (row labels)
    """
    
    def save_obj_to_file(self):
        
        if isinstance(self.obj, pandas.DataFrame):
            self.obj.to_csv(
                self.obj_file,
                sep = '\t', header = True, index = True)
        else:
            raise TypeError("Object should be instance of pandas.DataFrame but was %s"
                            % type(self.obj))

    def load_obj_from_file(self):

        self.obj = pandas.read_table(
            self.obj_file,
            sep = '\t', header = 0, index_col = 0)


    def add_to_version_info(self):
        
        self.version_info_h[ "PickMan version" ] = self.PickMan_ver
        self.version_info_h[ "Object type" ]     = "pandas.DataFrame"

if __name__ == "__main__":

    def functest(a, b, c, flag):
        h = [a, b, c, flag]
        return h

    pmI = Pickle_Manager(source_files = [ os.path.join(os.environ["RS_TMP_DIR"], "tmppm1.txt"),
                                          os.path.join(os.environ["RS_TMP_DIR"], "tmppm2.txt"),
                                          os.path.join(os.environ["RS_TMP_DIR"], "tmppm3.txt") ],
                         version_info_h = { "Ver major": "2.3", "Ver minor": "0.5" },
                         pkl_file = os.path.join(os.environ["RS_TMP_DIR"], "InterMed", "tmppm1.pkl"),
                         verbose = True,
                         ifunc = functest,
                         args = ["a", "b", "c"],
                         kwargs = { "flag" : True })

    print(pmI.get_obj())


    # This may not work for Python <= 2.6 as the class is using __getattr__
    class testclass:
        def __init__(self, h):
            self.h = h
        def __getattr__(self, attrname):
            if attrname == "__setstate__":
                raise AttributeError("%r object has no attribute %s" %
                                     (self.__class__, attrname))
            return getattr(self.h, attrname)


    pmI2 = Pickle_Manager(source_files = [ 'RSFPath("TMP", "tmppm1.txt")',
                                           os.path.join(os.environ["RS_TMP_DIR"], "tmppm2.txt"),
                                           os.path.join(os.environ["RS_TMP_DIR"], "tmppm3.txt") ],
                          version_info_h = { "Ver major": "2.3", "Ver minor": "0.5" },
                          pkl_file = os.path.join(os.environ["RS_TMP_DIR"], "InterMed", "tmppm2.pkl"),
                          verbose = True,
                          ifunc = testclass,
                          args = [{"a":"A", "bb":"BB", "ccc":"CCC"}],
                          kwargs = {})

    obj = pmI2.get_obj()
    print(type(obj), dir(obj), obj)
    print(type(pmI2), dir(pmI2))
    print(pmI2.get_update_flag())


    def functest3(tmp_x):
        tmpdfrm = \
            pandas.DataFrame([[1,2,3],
                              [4,5,tmp_x]])
        return tmpdfrm


    pmI3 = PDDFRM_Manager(source_files = [ 'RSFPath("TMP", "tmppm1.txt")',
                                           os.path.join(os.environ["RS_TMP_DIR"], "tmppm2.txt"),
                                           os.path.join(os.environ["RS_TMP_DIR"], "tmppm3.txt") ],
                          version_info_h = { "Ver major": "2.3", "Ver minor": "0.5" },
                          pkl_file = os.path.join(os.environ["RS_TMP_DIR"], "InterMed", "tmppm3.tsv"),
                          verbose = True,
                          ifunc = functest3,
                          args = [123],
                          kwargs = {})
    obj = pmI3.get_obj()
    print(obj)
