import numpy as np
import pyfits
from astropy.wcs import WCS
from skimage import measure

def edge_detect(im, hdr):
    w = WCS(hdr)
    ra = []
    dec = []
    exclude_RA = np.NaN
    exclude_DEC = np.NaN
    contours = measure.find_contours(im,0.5,fully_connected='high')
    x_pix = contours[0][:,0]
    y_pix = im.shape[1] - contours[0][:,1] - 1
    exclude_reg = np.array(contours).shape[0] - 1
    if exclude_reg > 0:
        i = 1
        exclude_RA = []
        exclude_DEC = []
        while i <= exclude_reg:
            x_excl = contours[i][:,0]
            y_excl = im.shape[1] - contours[i][:,1] - 1
            tmp_RA = []
            tmp_DEC = []
            for j in np.arange(len(x_excl)):
                x, y = w.wcs_pix2world(y_excl[j], x_excl[j], 0)
                tmp_RA.append(x.tolist())
                tmp_DEC.append(y.tolist())
            exclude_RA.append(tmp_RA)
            exclude_DEC.append(tmp_DEC)
            i += 1
    for i in np.arange(len(x_pix)):
        x, y = w.wcs_pix2world(y_pix[i], x_pix[i], 0)
        ra.append(x.tolist())
        dec.append(y.tolist())

    return ra, dec, exclude_RA, exclude_DEC
    


