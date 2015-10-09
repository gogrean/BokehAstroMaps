from binmap_manipulation import *
from edge_detector import edge_detect

root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"
binmap = root + "/contbin_binmap.fits"

BinIm, Hdr = read_binmap(binmap)

bins = find_bins(BinIm)
for bin in bins:
    RA, DEC = edge_detect(filter_bin(BinIm, bin), Hdr)
