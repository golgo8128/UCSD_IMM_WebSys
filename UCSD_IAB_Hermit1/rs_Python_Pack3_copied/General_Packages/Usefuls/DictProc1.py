#!/usr/bin/env python

import string
import sys
from collections import defaultdict

def list_count_dict(ilist):
    ret_dict = {}
    for elem in ilist:
        ret_dict[elem] = ret_dict.get(elem, 0) + 1
    return ret_dict

def dict_product(d1, d2, sep = "-"):
    ret_dict = {}
    for k1 in d1:
        for k2 in d2:
            k = k1 + sep + k2
            v = d1[k1] * d2[k2]
            ret_dict[k] = v

    return ret_dict

def list_product(l1, l2, sep = "-"):
    d1 = list_count_dict(l1)
    d2 = list_count_dict(l2)
    return dict_product(d1, d2, sep)

def count_dict_to_str(d, colon, sep):
        tlist = []
        for k in d:
                tlist.append(k + colon + repr(d[k]))
        return sep.join(tlist)

def count_dict_add(d1, d2):

    ret_d = {}

    for k1 in d1:
        ret_d[k1] = ret_d.get(k1, 0) + d1[k1]
    for k2 in d2:
        ret_d[k2] = ret_d.get(k2, 0) + d2[k2]

    return ret_d

def file_to_dict_simple(filename):
    fh = open(filename, "r")
    ret_dict = {}
    for line in fh:
        if not line.isspace():
            sline = line.rstrip()
            ret_dict[ sline ] = ""
    return ret_dict

def dict_to_file_simple(idict, filename, keyname = None, valname = None, sep = '\t'):
    fw = open(filename, "w")
    if keyname and valname:
        fw.write(sep.join((keyname, valname)) + '\n')
    for ikey in idict:
        fw.write(sep.join((str(ikey), str(idict[ikey]))) + '\n')

def rev_key_val(idict):
    odict = {}
    for k in idict:
        v = idict[k]
        odict[v] = k
    return odict

def rev_key_val_redund(idict):
    odict = {}
    for k in idict:
        v = idict[k]
        if v in odict:
            odict[v].append(k)
        else:
            odict[v] = [k]
    return odict


def rev_key_val_redund2(idict):

    odict = defaultdict(list)
    for ikey, ivalue in idict.items():
        odict[ ivalue ].append(ikey)

    return dict(odict)

def rev_dict_key_multivar(idict):
    
    odict = defaultdict(list)
    for ikey, ivalues in idict.items():
        for ivalue in ivalues:
            odict[ ivalue ].append(ikey)

    return dict(odict)    
    

def dict_to_list(idict):
    
    olist = []
    for ky in idict:
        olist.append((ky, idict[ky]))
    return olist

def dict_key_sort_accord_val(idict):

    return sorted(list(idict.keys()), key=lambda x:idict[x]) 


def dict_last_key_to_list(idict):
      
    rdict = {}
    try:
        for key in list(idict.keys()):
            odict = dict_last_key_to_list(idict[ key ])
            if odict is None:
                return list(idict.keys())
            else:
                rdict[ key ] = odict
        return rdict
            
    except AttributeError:
        return None
        

def dict_all_keys_in_depth(idict, depth = 0):
    
    if type(idict) is not dict:
        return set([])
    elif depth == 0:
        return set(idict.keys())
    else:
        okeys = set([])
        for ikey in idict:
            okeys |= dict_all_keys_in_depth(idict[ikey], depth - 1)
        return set(okeys)
            
def dict_all_keyvals_from_depth_sub(idict_sub, step_from_bottom = 0):
    
    if step_from_bottom == 0:
        return [ [[ okey ], idict_sub[ okey ]]
                 for okey in idict_sub ]
    else:
        ret = []
        for okey in idict_sub:
            sub_list = dict_all_keyvals_from_depth_sub(idict_sub[okey],
                                                       step_from_bottom - 1)
            ret += [ [[ okey ] + elem[0], elem[1]] for elem in sub_list]
        return ret
            
            
def dict_subset_key(idict, ikeys, check_exist = False):
    
    if check_exist:
        non_exist_keys = set(ikeys) - set(idict.keys())
        if non_exist_keys:
            raise Exception("Key(s) %s does not exist in the input dict." % ", ".join(list(non_exist_keys)))
            
    return dict((ik, idict[ik]) for ik in ikeys if ik in idict)


def dict_multdim_get(idict, multilayer_keys, default = None):
    
    cdict = idict
    for ikey in multilayer_keys:
        if ikey not in cdict:
            return default
        else:
            cdict = cdict[ikey]

    return cdict

def dict_val_to_len(idict):
    
    return dict([(ikey, len(idict[ikey])) for ikey in idict])
    

if __name__ == "__main__":

    import FileDirPath.TmpFile as TmpFile

    l1 = ["A", "B", "A", "C", "D", "C", "C" ]
    h = list_count_dict(l1)
    print(h)

    h1 = {"A":3, "B":2, "C":5 }
    h2 = {"D":2, "E":9, "A":7 }
    print(dict_product(h1, h2))

    l2 = ["C", "C", "X", "X", "X"]

    print(list_count_dict(l1))
    print(list_count_dict(l2))
    print(list_product(l1, l2))

    print(count_dict_to_str({"A": 5, "B":3, "C":2 }, ":", ","))

    h1 = count_dict_add(h1, h2)
    print(h1)

    from pprint import pprint
    
    print(dict_last_key_to_list(
        { "A" : { "apple" : "Ringo", "airplane" : "Hikoki" },
          "B" : { "banana" : "banana", "box" : "hako"},
          "C" : { "candy" : "ame", "coke" : "cola" }}))
    print(dict_all_keys_in_depth(
        { "A" : { "apple" : "Ringo", "airplane" : {"CCC" : True } },
          "B" : { "banana" : "banana", "box" : {"DDD" : True }},
          "C" : { "candy" : {"DDD" : True }, "coke" : "cola" }}, depth = 2))
    
    pprint(dict_all_keyvals_from_depth_sub(
        { "A" : { "apple" : "Ringo", "airplane" : {"CCC" : True } },
          "B" : { "banana" : "banana2", "box" : {"DDD" : True }},
          "C" : { "candy" : {"DDD" : True }, "coke" : "cola" }}, step_from_bottom = 1))
    
    
    testdic11 = {"A":10, "B":20, "CC":30, "D": 40}
    # print("--->", dict_subset_key(testdic11, ("A", "B", "XX", "YY"), True))


    tmp_obj = TmpFile.TmpFile_II("""
Monday
Tuesday
Wednesday
""")
    print(file_to_dict_simple(tmp_obj.filename()))
    
    print("Reverse hash")
    idict = { "A": 1, "B":2, "C":3, "D":2, "E": 1 }
    print(rev_key_val(idict))
    print(rev_key_val_redund(idict))
    print(rev_key_val_redund2(idict))
    print(dict_to_list(idict))
    print(dict_key_sort_accord_val(idict))
    dict_to_file_simple({"A": 1, "B": "b", "C": 3}, "/tmp/dictfiletmp1.tsv", "Col 1", "Col 2")
    
    idict = {"A":{"B": 1}, "C": {"D":{"E":33}}}
    print(dict_multdim_get(idict, ("C","D","E"), default = None))
    print(dict_multdim_get(idict, ("C","X","E"), default = "XXX"))
    
    idict2 = {"A": ["a","b","c"],
              "B": ["a","b","d"],
              "C": ["c","d","e","f"]}
    print(rev_dict_key_multivar(idict2))
    print(dict_val_to_len(idict2))
    