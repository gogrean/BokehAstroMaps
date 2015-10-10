from binmap_manipulation import read_binmap
from xcm import grab_data

root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"
binmap = root + "/contbin_binmap.fits"

BinIm, Hdr = read_binmap(binmap)

data = grab_data(BinIm, Hdr, root, 11, 'kT')

output_file("MACSJ1149_Tmap.html", title="Temperature map of MACS J1149.6-2223")

TOOLS="pan,wheel_zoom,box_zoom,reset,hover,save"
p = figure(title="Temperature map of MACS J1149.6-2223", tools=TOOLS)

p.patches('RA', 'DEC',
    fill_color='blue', fill_alpha=0.7,
    line_color="white", line_width=0.5,
    source=data)

hover = p.select(dict(type=HoverTool))
hover.point_policy = "follow_mouse"
hover.tooltips = OrderedDict([
    ("Bin number: ", "@bin"),
    ("Temperature: ", "@p"),
    ("(RA, DEC)", "($RA, $DEC)"),
])

show(p)

