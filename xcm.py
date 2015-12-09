import re
import numpy as np
import math
from binmap_manipulation import *
from edge_detector import *

def read_param(XCMfile, param):
    seq = " " * 7
    start_at = 7 - len(str(param))
    seq = "#" + seq[1:start_at] + str(param)
    for line in reversed(list(open(XCMfile))):
        if seq == line[:7]:
            out = re.split(r"[,\(\)\n ]+", line)
            p_min, p_max = float(out[2]), float(out[3])
            perr_lo, perr_hi = float(out[4]), float(out[5])
            p = p_min - perr_lo
            break
    return p, perr_lo, perr_hi

def grab_data(BinIm, Hdr, XCMroot, param):
    data = {}
    bins = find_bins(BinIm)
    for bin in bins:
        ThreshIm = filter_bin(BinIm, bin)
        XCMfile = XCMroot + "/xaf_" + str(bin) + ".log"
        ra, dec, exclude_RA, exclude_DEC = edge_detect(ThreshIm, Hdr)
        p, perr_lo, perr_hi = read_param(XCMfile, param)
        if type(exclude_RA) is list:
            exclude_RA.insert(0, ra)
            ra = exclude_RA
            exclude_DEC.insert(0, dec)
            dec = exclude_DEC
        data[bin] = {
            'bin': bin,
            'RA': ra,
            'Dec': dec,            
            'best-fit': p,
            'err_lo': perr_lo,
            'err_hi': perr_hi
        }

    return data
    


            
