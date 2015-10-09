import pyfits

def read_binmap(ImFile):
    hdu = pyfits.open(ImFile)
    hdr = hdu[0].header
    del hdr['COMMENT']
    del hdr['HISTORY']
    BinIm = hdu[0].data
    return BinIm, hdr

def filter_bin(im, bin):
    im[im != bin] = 0
    im[im == bin] = 1
    return im

