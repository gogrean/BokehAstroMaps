'''
Import RH data from RH_clusters.csv.
'''

from __future__ import division

import pandas as pd
import numpy as np
from uncertainties import ufloat, unumpy, umath

def import_RHdata(file):
    halos = pd.read_csv(file)
    return halos

def filter_clusters(file, categories=["Limit+SZ", "Limit-SZ", "RHclusters"]):
    data = import_RHdata(file)
    clusters = {}
    clusters["Limit+SZ"] = data[(data["RadioLimit?"] == True) & (data["WithSZ?"] == True)]
    clusters["Limit-SZ"] = data[(data["RadioLimit?"] == True) & (data["WithSZ?"] == False)]
    clusters["RHclusters"] = data[(data["RadioLimit?"] == False) & (data["WithSZ?"] == True)]
    return clusters

def lx_range(lx_min, lx_max):
    return np.logspace(np.log10(lx_min), np.log10(lx_max), num=1000)

def fitting_powerlaw_LP(lx_min, lx_max,
        const=[ufloat(0.083,0.058), ufloat(2.11,0.21)]):
    x = lx_range(lx_min, lx_max)
    y = (10**24.5) * ((x/1e45)**const[1]) * (10**const[0])
    y_nom = unumpy.nominal_values(y)
    y_min = unumpy.nominal_values(y) - unumpy.std_devs(y)
    y_max = unumpy.nominal_values(y) + unumpy.std_devs(y)
    return y_nom, y_min, y_max

def fitting_powerlaw_YP(sz_min, sz_max,
        const=[ufloat(-0.133,0.069), ufloat(2.03,0.30)]):
    x = lx_range(sz_min, sz_max)
    y = (10**24.5) * ((x/1e-4)**const[1]) * (10**const[0])
    y_nom = unumpy.nominal_values(y)
    y_min = unumpy.nominal_values(y) - unumpy.std_devs(y)
    y_max = unumpy.nominal_values(y) + unumpy.std_devs(y)
    return y_nom, y_min, y_max


# p.circle(x=lx_arr/1e44, y=pow_nom/1e24, color="#36454F", fill_alpha=0.1, size=10)
# p.patch(x='lx', y='pow', color="#36454F", fill_alpha=0.25, source=source)
