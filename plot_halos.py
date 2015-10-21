import pandas as pd
import numpy as np
from uncertainties import ufloat, unumpy, umath

from collections import OrderedDict
from bokeh.plotting import ColumnDataSource, figure, show, output_file, gridplot
from bokeh.models import HoverTool, Plot

from build_data import *
from halos import *

def plot_LP(clusters, categories = ["Limit+SZ", "Limit-SZ", "RHclusters"],
        colors=['#462066', '#00AAA0', '#FF7A5A'],
        title='L-P Relation for Radio Halo Clusters',
        xaxis_label='0.1-2.4 keV X-ray Luminosity (x 1E+44 erg/s)',
        yaxis_label='1.4 GHz Radio Halo Power (x 1E+24 W/Hz)',
        label_font_size='14pt', title_font_size='16pt',
        x_range=[1, 50], y_range=[0.1,100], xsize=600, ysize=600,
        x_axis_type="log", y_axis_type="log",
        legend=["Upper limits on RH power, with SZ",
            "Upper limits on RH power, no SZ", "RH detections"],
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,hover,hover,hover,previewsave"
        ):

    p1 = figure(width=xsize, height=ysize,
        title=title, title_text_font_size=title_font_size,
        x_axis_type=x_axis_type, y_axis_type=y_axis_type,
        x_range=x_range, y_range=y_range, tools=TOOLS)
    p1.xaxis.axis_label = xaxis_label
    p1.yaxis.axis_label = yaxis_label
    p1.xaxis.axis_label_text_font_size = label_font_size
    p1.yaxis.axis_label_text_font_size = label_font_size

    tooltips0, extra_tooltips = BuildTooltips()

    index = 0
    for cat in categories:
        source = BuildDataSource(clusters,cat)
        if index <= 1:
            f = p1.inverted_triangle(x='lx', y='pow', size=15, color=colors[index],
                    fill_alpha=0.75, line_color=colors[index], line_width=2,
                    legend=legend[index], source=source)
            hover = p1.select(dict(type=HoverTool))
            hover[index].renderers = [f]
            hover[index].tooltips = tooltips0 + extra_tooltips[index]
        else:
            f = p1.circle(x='lx', y='pow', size=20, color=colors[index],
                    fill_alpha = 0.75, line_color=colors[index], line_width=2,
                    legend=legend[index], source=source)
            hover = p1.select(dict(type=HoverTool))
            hover[index].renderers = [f]
            hover[index].tooltips = tooltips0 + extra_tooltips[index]
        index += 1

    lx_min, lx_max = 1e43, 1e46
    lx_arr = lx_range(lx_min,lx_max)
    pow_nom, pow_min, pow_max = fitting_powerlaw_LP(lx_min,lx_max)

    ln = p1.line(x=lx_arr/1e44, y=pow_nom/1e24, color="#36454F", line_width=3)
    hover = p1.select(dict(type=HoverTool))
    hover[index].renderers = [ln]
    hover[index].tooltips = ("log(L/1e44 erg/s) = B log(P/1e24 W/Hz) + A")
    y = list(pow_min/1e24)
    y.extend(list(reversed(list(pow_max/1e24))))
    x = list(lx_arr/1e44)
    x.extend(list(reversed(list(lx_arr/1e44))))
    p1.patch(x=x, y=y, color="#36454F", fill_alpha=0.25)

    p1.legend.orientation = "top_left"
    p1.legend.label_text_font = "times"
    p1.legend.label_text_color = "#36454F"
    p1.legend.label_text_font_size = "14pt"

    return p1

def plot_YP(clusters, categories = ["Limit+SZ", "Limit-SZ", "RHclusters"],
    colors=['#462066', '#00AAA0', '#FF7A5A'],
    title='Y-P Relation for Radio Halo Clusters',
    xaxis_label='SZ Y Value (x 1E-04 Mpc\u00B2)',
    yaxis_label='1.4 GHz Radio Halo Power (x 1E+24 W/Hz)',
    label_font_size='14pt', title_font_size='16pt',
    x_range=[0.2,6], y_range=[0.1,100], xsize=600, ysize=600,
    x_axis_type="log", y_axis_type="log",
    legend=["Upper limits on RH power, with SZ",
        "Upper limits on RH power, no SZ", "RH detections"],
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,hover,hover,previewsave",
    withLP=False
    ):

    p2 = figure(width=xsize, height=ysize,
        title=title, title_text_font_size=title_font_size,
        x_axis_type=x_axis_type, y_axis_type=y_axis_type,
        x_range=x_range, y_range=y_range, tools=TOOLS)
    p2.xaxis.axis_label = xaxis_label
    p2.yaxis.axis_label = yaxis_label
    p2.xaxis.axis_label_text_font_size = label_font_size
    p2.yaxis.axis_label_text_font_size = label_font_size

    tooltips0, extra_tooltips = BuildTooltips()

    index = [0,2]
    for ii in index:
        cat = categories[ii]
        source = BuildDataSource(clusters,cat)
        if ii == 0:
            f = p2.inverted_triangle(x='y500', y='pow', size=15, color=colors[ii],
                    fill_alpha=0.75, line_color=colors[ii], line_width=2,
                    legend=legend[ii], source=source)
            hover = p2.select(dict(type=HoverTool))
            hover[ii].renderers = [f]
            hover[ii].tooltips = tooltips0 + extra_tooltips[ii]
        else:
            f = p2.circle(x='y500', y='pow', size=20, color=colors[ii],
                    fill_alpha = 0.75, line_color=colors[ii], line_width=2,
                    legend=legend[ii], source=source)
            hover = p2.select(dict(type=HoverTool))
            hover[ii-1].renderers = [f]
            hover[ii-1].tooltips = tooltips0 + extra_tooltips[ii]

    sz_min, sz_max = 1e-5, 1e-3
    sz_arr = lx_range(sz_min,sz_max)
    pow_nom, pow_min, pow_max = fitting_powerlaw_YP(sz_min,sz_max)

    ln = p2.line(x=sz_arr/1e-4, y=pow_nom/1e24, color="#36454F", line_width=3)
    hover = p2.select(dict(type=HoverTool))
    print(ii)
    hover[ii].renderers = [ln]
    hover[ii].tooltips = ("log(Y/1e-4 Mpc\u00B2) = B log(P/1e24 W/Hz) + A")

    p2.legend.orientation = "top_left"
    p2.legend.label_text_font = "times"
    p2.legend.label_text_color = "#36454F"
    p2.legend.label_text_font_size = "14pt"

    return p2


def plot_LP_YP(file, outfile='Lx-P.html',
      title='L-P Relation for Radio Halo Clusters',
      categories = ["Limit+SZ", "Limit-SZ", "RHclusters"],
      colors=['#462066', '#00AAA0', '#FF7A5A'],
      xaxis_label='0.1-2.4 keV X-ray Luminosity (x 1E+44 erg/s)',
      yaxis_label='1.4 GHz Radio Halo Power (x 1E+24 W/Hz)',
      label_font_size='14pt', title_font_size='16pt',
      x_range=[1, 50], y_range=[0.1,100], xsize=600, ysize=600,
      x_axis_type="log", y_axis_type="log",
      legend=["Upper limits on RH power, with SZ",
        "Upper limits on RH power, no SZ", "RH detections"],
      TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,hover,hover,hover,previewsave",
      withSZ=False, withLP=True):

    clusters = filter_clusters(file)
    output_file(outfile, title=title)


    if withSZ == True and withLP == True:
        p1 = plot_LP(clusters)
        p2 = plot_YP(clusters)
        p2.y_range = p1.y_range
        p = gridplot([[p1,p2]], toolbar_location='above')
        show(p)
    elif withLP != True and withSZ == True:
        p2 = plot_YP(clusters)
        show(p2)
    elif withLP == True and withSZ != True:
        p1 = plot_LP(clusters)
        show(p1)

plot_LP_YP("RH_clusters.csv", withLP=True, withSZ=True)
