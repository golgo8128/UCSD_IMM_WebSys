#!/usr/bin/env python

import time


def gen_uniq_stamp_based_on_time(stamp = None):
    
    stamp_proto = hex(int(time.time() * 100000))[2:]
    # Try:
    #    for i in range(100): print(hex(int(time.time() * 100000))) on server,
    # and see how fast your server processing is.
    
    if not stamp:
        stamp = stamp_proto
    elif "%s" in stamp:
        stamp = stamp % stamp_proto
    
    return stamp

    
if __name__ == "__main__":
    print(gen_uniq_stamp_based_on_time())
    print(gen_uniq_stamp_based_on_time("XXX"))
    print(gen_uniq_stamp_based_on_time("ABC: %s"))
    