#!/usr/bin/evn python
'''
Created on May 3, 2011

@author: rsaito
'''

def strjoin_cut(ilist, delimiter, secsize):
    """ delimiter containing space at the end not recommended (ex. delimiter = ", ") """
    
    ostr = ""
    for pos in range(len(ilist)):
        ostr += ilist[pos]
        if pos != len(ilist) - 1:
            ostr += delimiter
            if pos > 0 and (pos+1) % secsize == 0:
                ostr += '\n'
    
    return ostr

def strjoin_max(ilist, isep = ",", imax = 10,
                dots_str = "..."):

    if imax < 0:
        raise Exception("Negative value given as maximum items to display")
    
    if len(ilist) == 0:
        return ""
    if imax == 0:
        return dots_str
    
    # From here, assume that len(ilist) > 0 and imax > 0
    
    if len(ilist) == 1:
        return ilist[0]
    
    # From here, assume that len(ilist) > 1 and imax > 0
    if imax == 1:
        return isep.join([ilist[0]] + [dots_str])

    # From here, assume that len(ilist) > 1 and imax > 1
       
    tail_segm = 3
      
    if len(ilist) > imax:    
        left_end = imax - tail_segm
        if left_end <= 0:
            left_end = imax - 1
        elif left_end < tail_segm and tail_segm < imax:
            left_end = tail_segm
        right_start = len(ilist) - tail_segm
        if left_end >= right_start:
            right_start = left_end 
        if left_end + (len(ilist) - right_start) > imax:
            right_start = len(ilist) - (imax - left_end) 
            
        return isep.join(ilist[0:left_end] + [dots_str] + ilist[right_start:])

    return isep.join(ilist)


if __name__ == "__main__":
    print(strjoin_cut(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"], ",", 5))
    print("---")
    print(strjoin_cut(["a","b"], ",", 5))

    print(strjoin_max(["a","b","c","d","e","f","g","h","i","j"], ',', 2))    
    print(strjoin_max(["a","b","c","d","e","f","g","h","i","j"], ',', 5))
    print(strjoin_max(["a","b","c","d","e","f","g","h","i","j","k","l","m"], ',', 10))
    
    