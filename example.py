from idv_plot import plot_patches

# Directory where the bin map and Xspec log files are located.
root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"

# File name of the bin map.
binmap = "contbin_binmap.fits"

# Point source regions included in bin map?
# True if yes, False otherwise.
point_sources = False


# Output html file name and title.
out = "MACSJ1149_Tmap.html"
out_title = "Temperature Map of MACS J1149.6-2223"

# Plot style.
title_font_size = '16pt'
label_font_size = '14pt'
xaxis_label = "RA (J2000)"
yaxis_label = "Dec (J2000)"

# Number of the Xspec parameter being plotted.
xcm_id = 11

# Parameter description.
xcm_param = 'Temperature'

# Units of the parameter.
xcm_units = 'keV'

# Colormap properties.

# Colormap name. Default is 'coolwarm', in which cold regions are blue and hot regions are red.
cmap = 'coolwarm'

# Colormap limits. By default, these are min(parameter) and max(parameter). 
vmin = None
vmax = None


plot_patches(root, binmap, xcm_id, point_sources=point_sources,
        out=out, out_title=out_title,
        title_font_size=title_font_size, label_font_size=label_font_size,
        xcm_param=xcm_param, xcm_units=xcm_units,
        xaxis_label=xaxis_label, yaxis_label=yaxis_label, palette=cmap, vmin=vmin, vmax=vmax)


