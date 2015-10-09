import numpy as np
import pyfits
from astropy.wcs import WCS

def find_neighbors(im, xcoord, ycoord):
    neighbors = []
    rows, cols = im.shape[0], im.shape[1]
    for x,y in [(xcoord+i,ycoord+j) for i in [-1,0,1] for j in [-1,0,1] if abs(i) != abs(j)]:
        if x in np.arange(rows) and y in np.arange(cols):
            neighbors.extend([x,y])
    return neighbors

def edge_detect(im, hdr):
    w = WCS(hdr)
    rows = im.shape[0]
    cols = im.shape[1]
    reg = np.argwhere(im != 0)
    ra_edge = []
    dec_edge = []
    for (x,y) in reg:
        if 0 in im[find_neighbors(im,x,y)]:
            x_edge, y_edge = w.wcs_pix2world(y,x,0)
            ra_edge.append(float(x_edge))
            dec_edge.append(float(y_edge))
    return ra_edge, dec_edge


