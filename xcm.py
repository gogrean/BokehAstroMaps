import re
from binmap_manipulation import *
from edge_detector import edge_detect
from bokeh.plotting import ColumnDataSource

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

def grab_data(BinIm, Hdr, XCMroot, param, param_description):
    data = {}
    bins = find_bins(BinIm)
    for bin in bins:
        XCMfile = XCMroot + "/xaf_" + str(bin) + ".log"
        ra, dec = edge_detect(filter_bin(BinIm, bin), Hdr)
        p, perr_lo, perr_hi = read_param(XCMfile, param)
        data[bin] = {
            'bin': bin,
            'RA': ra,
            'Dec': dec,            
            'param': param_description,
            'best-fit': p,
            'err_lo': perr_lo,
            'err_hi': perr_hi
        }
    return ColumnDataSource(data)
    


            