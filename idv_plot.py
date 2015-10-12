import numpy as np
import matplotlib.pyplot as plt
from binmap_manipulation import read_binmap
from xcm import grab_data
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool

def plot_patches(root, binmap, xcm_id, point_sources=True, 
        out='bokeh_map.html', out_title='',
        title_font_size='16pt', label_font_size='14pt',
        xcm_param='XCM parameter', xcm_units='',
        xaxis_label='RA (J2000)', yaxis_label='Dec (J2000)',
        palette=None, vmin=None, vmax=None):

    BinIm, Hdr = read_binmap(root + "/" + binmap)
    MapInfo = grab_data(BinIm, Hdr, root, xcm_id, point_sources=point_sources)

    output_file(out, title=out_title)

    TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"
    p = figure(
    title = out_title, 
    title_text_font_size = title_font_size,
    tools = TOOLS)

    ra = [MapInfo[bin]['RA'] for bin in MapInfo]
    dec = [MapInfo[bin]['Dec'] for bin in MapInfo]

    bins = []
    param = []
    perr_lo = []
    perr_hi = []
    for bin in MapInfo:
        bins.append(MapInfo[bin]['bin'])
        param.append(MapInfo[bin]['best-fit'])
        perr_lo.append(MapInfo[bin]['err_lo'])
        perr_hi.append(MapInfo[bin]['err_hi'])

    if palette:
        colors = values_to_palette(param, cmap=palette, vmin=vmin, vmax=vmax)
    else:
        colors = 'blue'
            
    source = ColumnDataSource(
        data = dict(
            x = ra,
            y = dec,
            bin = bins,
            param = param,
            color = colors,
            perr_lo = perr_lo,
            perr_hi = perr_hi
        )
    )

    p.patches(xs = 'x',ys = 'y',
        fill_color='color', fill_alpha=0.75,
        line_color="white", line_width=0.33,
        source=source)
    p.xaxis.axis_label = xaxis_label
    p.xaxis.axis_label_text_font_size = label_font_size
    p.yaxis.axis_label = yaxis_label
    p.yaxis.axis_label_text_font_size = label_font_size

    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = OrderedDict([
        ("Bin number", "@bin"),
        (xcm_param, "@param (@perr_lo, @perr_hi) " + xcm_units),
        ("(RA, Dec)", "($x, $y)")
    ])

    show(p)

def values_to_palette(values, cmap='coolwarm', vmin=None, vmax=None):
    color_map = plt.get_cmap(cmap)
    if not vmin:
        vmin = np.min(values)
    if not vmax:
        vmax = np.max(values)
    colors = []
    for val in values:
        color = color_map((val-vmin)/(vmax-vmin))
        r, g, b = color[0]*255., color[1]*255., color[2]*255.
        color = '#%02x%02x%02x' % (r,g,b)
        colors.append(color)
    return colors