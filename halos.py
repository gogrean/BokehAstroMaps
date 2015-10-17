'''
Import RH data from RH_clusters.csv.
'''

from __future__ import division

import pandas as pd
import numpy as np
from uncertainties import ufloat, unumpy, umath

from collections import OrderedDict
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models import HoverTool, Plot

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

def fitting_powerlaw(lx_min, lx_max, const=[ufloat(0.083,0.058), ufloat(2.11,0.21)]):
    x = lx_range(lx_min, lx_max)
    y = (10**24.5) * ((x/1e45)**const[1]) * (10**const[0])
    y_nom = unumpy.nominal_values(y)
    y_min = unumpy.nominal_values(y) - unumpy.std_devs(y)
    y_max = unumpy.nominal_values(y) + unumpy.std_devs(y)
    return y_nom, y_min, y_max
 
 
 
def plot_clusters(file, categories = ["Limit+SZ", "Limit-SZ", "RHclusters"],
        colors=['#462066', '#00AAA0', '#FF7A5A'], 
        outfile='Lx-P.html', title='L-P Relation for Radio Halo Clusters',
        xaxis_label='0.1-2.4 keV X-ray Luminosity (x 1E+44 erg/s)',
        yaxis_label='1.4 GHz Radio Halo Power (x 1E+24 W/Hz)',
        label_font_size='14pt', title_font_size='16pt'):

    clusters = filter_clusters(file)
    output_file(outfile, title=title)
    
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,hover,hover,hover,previewsave"
    p = figure(title=title, title_text_font_size=title_font_size, 
        x_axis_type="log", y_axis_type="log", 
        x_range=[1, 50], y_range=[0.1,100], tools=TOOLS)
    p.xaxis.axis_label = xaxis_label
    p.yaxis.axis_label = yaxis_label
    p.xaxis.axis_label_text_font_size = label_font_size
    p.yaxis.axis_label_text_font_size = label_font_size

    legend = ["Upper limits on RH power, with SZ", "Upper limits on RH power, no SZ", "RH detections"]

    index = 0
    tooltips0 = [
        ("Cluster", "\u2002 @cluster"),
        ("(RA, Dec)", "\u2002 (@x, @y)"),
        ("L [0.1-2.4 keV]", "\u2002 (@lx \u00B1 @lx_err) x 1E+44 erg/s")
    ]
    extra_tooltips = []
    extra_tooltips.append([
        ("P [1.4 GHz]", "\u2264 @pow x 1E+24 W/Hz"),
        ("YSZ", "\u2002 (@y500 \u00B1 @y500_err) x 1E-04 Mpc\u2009\u00B2")
    ])
    extra_tooltips.append([
        ("P [1.4 GHz]", "\u2264 @pow x 1E+24 W/Hz"),
    ])
    extra_tooltips.append([
        ("P [1.4 GHz]", "\u2002 (@pow \u00B1 @pow_err) x 1E+24 W/Hz"),
        ("YSZ", "\u2002 (@y500 \u00B1 @y500_err) x 1E-04 Mpc\u2009\u00B2")
    ])
    for cat in categories:
        source = ColumnDataSource(
            data = dict(
                x = clusters[cat]['RA'],
                y = clusters[cat]['DEC'],
                cluster = clusters[cat]['CLUSTER'],
                z = clusters[cat]['REDSHIFT'],
                lx = clusters[cat]['0.1-2.4 keV X-ray Luminosity (x 1E+44 erg/s)'],
                lx_err = clusters[cat]['LX_err'],
                pow = clusters[cat]['1.4 GHz Radio Power (x 1E+24 W/Hz)'],
                pow_err = clusters[cat]['P14_err'],
                y500 = clusters[cat]['SZ'],
                y500_err = clusters[cat]['SZ_err']
            )
        )
        if index <= 1:
            f = p.inverted_triangle(x='lx', y='pow', size=15, color=colors[index],
                    fill_alpha=0.75, line_color=colors[index], line_width=2, 
                    legend=legend[index], source=source) 
            hover = p.select(dict(type=HoverTool))
            hover[index].renderers = [f]
            hover[index].tooltips = tooltips0 + extra_tooltips[index]
        else:
            f = p.circle(x='lx', y='pow', size=20, color=colors[index],
                    fill_alpha = 0.75, line_color=colors[index], line_width=2, 
                    legend=legend[index], source=source)
            hover = p.select(dict(type=HoverTool))
            hover[index].renderers = [f]
            hover[index].tooltips = tooltips0 + extra_tooltips[index]
        index += 1
    
    lx_min, lx_max = 1e43, 1e46
    lx_arr = lx_range(lx_min,lx_max)
    pow_nom, pow_min, pow_max = fitting_powerlaw(lx_min,lx_max)

    ln = p.line(x=lx_arr/1e44, y=pow_nom/1e24, color="#36454F", line_width=3)
#    ln = p.line(x=[1.,50.], y=[0.1,100.], color="#36454F", line_width=3)
    hover = p.select(dict(type=HoverTool))
    hover[index].renderers = [ln]
    hover[index].tooltips = ("log(L/1e44 erg/s) = B log(P/1e24 W/Hz) + A")
    
    p.legend.orientation = "top_left"
    p.legend.label_text_font = "times"
    p.legend.label_text_color = "#36454F"
    p.legend.label_text_font_size = "14pt"
    
    show(p)

plot_clusters('RH_clusters.csv')

# p.circle(x=lx_arr/1e44, y=pow_nom/1e24, color="#36454F", fill_alpha=0.1, size=10)    
# p.patch(x='lx', y='pow', color="#36454F", fill_alpha=0.25, source=source)


