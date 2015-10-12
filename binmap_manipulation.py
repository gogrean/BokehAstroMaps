import pyfits
import numpy as np

def read_binmap(ImFile):
    hdu = pyfits.open(ImFile)
    hdr = hdu[0].header
    del hdr['COMMENT']
    del hdr['HISTORY']
    BinIm = hdu[0].data
    return BinIm, hdr

def filter_bin(im, bin):
    imcopy = im.copy()
    imcopy[im == bin] = 1
    imcopy[im != bin] = 0
    pyfits.writeto('bin'+str(bin)+'.fits',imcopy,clobber=True)
    return imcopy
    
def find_bins(im):
    bins = []
    maxbin = np.max(im)
    [bins.append(i) for i in np.arange(maxbin+1) if i in im]
    return bins



