#!/usr/bin/env python
'''
Created on 2014/02/02

@author: rsaito
'''

import re
# from ListProc1 import pair_list_to_dict
from collections import OrderedDict

pat_sec = re.compile(r"^\[\s*(\S.*\S)\s*\]|^\[\s*(\S)\s*\]")


def simple_array_hash_file1(savefile, info_h = None):

    if info_h:
        fh = open(savefile, 'w')
        ct = 0
        for ikey in info_h:
            ival = info_h[ikey];

            if ct:
                fh.write('\n')
            fh.write('[ %s ]\n' % ikey)

            if type(ival) is list or type(ival) is tuple:
                fh.writelines([ eline + '\n' for eline in ival])
            elif type(ival) is dict or type(ival) is OrderedDict:
                for subkey in ival:
                    fh.write("%s\t%s\n" % (subkey, ival[subkey]))
            else:
                raise TypeError("Illegal data type: %s", type(ival))

            ct = ct + 1
    else:
        info_h = OrderedDict()

        fh = open(savefile, 'r');

        sec_name = ""
        sec_mode = ""

        tline = fh.readline()

        while tline:
            search_res = pat_sec.search(tline)
            if search_res:
                sec_pat = search_res.group(1) or search_res.group(2)
            else:
                sec_pat = None

            if sec_pat:
                sec_name = sec_pat.strip()
                sec_mode = ""
            elif tline and not tline.isspace() and not tline.startswith('#'):
                strs = tline.split('\t')
                if len(strs) == 1:
                    if not sec_mode:
                        sec_mode = "array"
                        info_h[sec_name] = [ strs[0].rstrip() ]
                    elif sec_mode == "array":
                        info_h[sec_name].append(strs[0].rstrip())
                    else:
                        raise TypeError("Multiple forms in section %s" % sec_name)
                else:
                    if not sec_mode:
                        sec_mode = 'hash'
                        info_h[sec_name] = OrderedDict(((strs[0].rstrip(), strs[1].strip()),))
                    elif sec_mode == "hash":
                        info_h[sec_name][ strs[0].rstrip() ] = strs[1].strip()
                    else:
                        raise TypeError("Multiple forms in section %s" % sec_name)

            tline = fh.readline()


    fh.close()
    return info_h


def simple_array_hash_to_str(info_h):
    
    ostr = ""
    
    ct = 0
    for ikey in info_h:
        ival = info_h[ikey];

        if ct:
            ostr += '\n'
        ostr += '[ %s ]\n' % ikey

        if type(ival) is list or type(ival) is tuple:
            ostr += '\n'.join([ eline for eline in ival]) + '\n'
        elif type(ival) is dict or type(ival) is OrderedDict:
            for subkey in ival:
                ostr += "%s\t%s\n" % (subkey, ival[subkey])
        else:
            raise TypeError("Illegal data type: %s", type(ival))

        ct = ct + 1    
        
    return ostr


if __name__ == "__main__":
    #===========================================================================
    # print simple_array_hash_file1("/Users/rsaito/Desktop/tmp11.txt",
    #                               { "Section 1" : ["Item 1", "Item 2", "Item 3"],
    #                                 "Section 2" : { "Version major": "1.2", "Version minor": "0.7" },
    #                                 "Section 3" : ["Item 4", "Item 5"]})
    #===========================================================================
    # print simple_array_hash_file1("/Users/rsaito/Desktop/tmp11.txt")


    import FileDirPath.TmpFile
    from pprint import pprint
    
    tmp_obj1 = FileDirPath.TmpFile.TmpFile_II("""
[ sfiles ]
/Users/rsaito/Desktop/tmp11.txt
/Users/rsaito/Desktop/tmp12.txt
/Users/rsaito/Desktop/tmp13.txt
/Users/rsaito/Desktop/tmp14.txt
/Users/rsaito/Desktop/tmp15.txt

[ versions ]
version 1.2
type F
""")

    pprint(simple_array_hash_file1(tmp_obj1.filename()))

    tmp_obj2 = FileDirPath.TmpFile.TmpFile_II("""
[ sfiles ]
/Users/rsaito/Desktop/tmp11.txt
/Users/rsaito/Desktop/tmp12.txt
/Users/rsaito/Desktop/tmp13.txt
/Users/rsaito/Desktop/tmp14.txt
/Users/rsaito/Desktop/tmp15.txt

[ versions ]
version\t1.2
type\tF
""")

    pprint(simple_array_hash_file1(tmp_obj2.filename()))
    
    tmp_obj3 = FileDirPath.TmpFile.TmpFile_II("""
[ sfiles ]
*
[ versions ]
version\t1.2
type\tF
# Hello! No space allowed before sharp.
type2\tT
""")

    pprint(simple_array_hash_file1(tmp_obj3.filename()))

    print("- - - - -")

    print(simple_array_hash_to_str(simple_array_hash_file1(tmp_obj3.filename())))

    print("- - - - -")

    tmp_h = simple_array_hash_file1(tmp_obj2.filename())
    pprint(tmp_h)
    simple_array_hash_file1(tmp_obj2.filename(), tmp_h)
    print("".join([ iline for iline in open(tmp_obj2.filename()) ]))
    # print(tmp_obj2.filename())
    