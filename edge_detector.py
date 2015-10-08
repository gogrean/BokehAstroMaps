import numpy as np
import pyfits
from astropy.wcs import WCS

def find_neighbors(im,xcoord,ycoord):
    im = pyfits.getdata(im,0)
    neighbors = []
    rows, cols = im.shape[0], im.shape[1]
    for x,y in [(xcoord+i,ycoord+j) for i in [-1,0,1] for j in [-1,0,1] if abs(i) != abs(j)]:
        if x in np.arange(rows) and y in np.arange(cols):
            neighbors.extend([x,y])
    return neighbors

def edge_detect(ImFile):
    w = WCS(ImFile)
    im = pyfits.getdata(ImFile,0)
    rows = im.shape[0]
    cols = im.shape[1]
    reg = np.argwhere(im != 0)
    ra_edge = []
    dec_edge = []
    for (x,y) in reg:
        if 0 in im[find_neighbors(ImFile,x,y)]:
            x_edge, y_edge = w.wcs_pix2world(y,x,0)
            ra_edge.append(float(x_edge))
            dec_edge.append(float(y_edge))
    return ra_edge, y_edge

def filter_bin(im,bin):
    im, hdr = pyfits.getdata(im,0, header=True)
    im[im != bin] = 0
    im[im == bin] = 1
    pyfits.writeto("bin"+str(bin)+".fits", im, header=hdr, clobber=True)

# Move this stuff to a tests directory
root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"
filter_bin(root+"/contbin_binmap.fits", 1)
edge_detect("bin1.fits")

