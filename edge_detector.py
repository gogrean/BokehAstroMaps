import numpy as np
import pyfits
from astropy.wcs import WCS
from skimage import measure

def edge_detect(im, hdr):
    w = WCS(hdr)
    ra = []
    dec = []
    contours = measure.find_contours(im,0.5,fully_connected='high')
    x_pix = contours[0][:,0]
    y_pix = im.shape[1] - contours[0][:,1] - 1
    exclude = False
    if len(contours) >= 5:
        exclude = True
    for i in np.arange(len(x_pix)):
        x, y = w.wcs_pix2world(y_pix[i], x_pix[i], 0)
        ra.append(x)
        dec.append(y)
    return ra, dec, exclude
    


