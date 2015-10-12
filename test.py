from binmap_manipulation import read_binmap
from xcm import grab_data
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool

root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"
binmap = root + "/contbin_binmap.fits"

BinIm, Hdr = read_binmap(binmap)

MapInfo = grab_data(BinIm, Hdr, root, 11, 'kT')

output_file("MACSJ1149_Tmap.html", title="Temperature Map of MACS J1149.6-2223")

TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"
p = figure(
    title = "Temperature Map of MACS J1149.6-2223", 
    title_text_font_size = '16pt',
    tools = TOOLS    
)

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
    
source = ColumnDataSource(
    data = dict(
        x = ra,
        y = dec,
        bin = bins,
        param = param,
        perr_lo = perr_lo,
        perr_hi = perr_hi
    )
)


p.patches(xs = 'x',ys = 'y',
      fill_color='blue', fill_alpha=0.7,
      line_color="white", line_width=0.5,
      source=source)
p.xaxis.axis_label = "RA (J2000)"
p.xaxis.axis_label_text_font_size = "14pt"
p.yaxis.axis_label = "Dec (J2000)"
p.yaxis.axis_label_text_font_size = "14pt"

hover = p.select(dict(type=HoverTool))
hover.point_policy = "follow_mouse"
hover.tooltips = OrderedDict([
    ("Bin number: ", "@bin"),
    ("Temperature: ", "@param (@perr_lo, @perr_hi) keV"),
    ("(RA, Dec): ", "($x, $y)")
])

show(p)

