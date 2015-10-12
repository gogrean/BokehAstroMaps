from idv_plot import plot_patches

# Directory where the bin map is located.
root = "/Users/gogrean/data/from_calypso/chandra/macsj1149/merged7"

# File name of the bin map.
binmap = "contbin_binmap.fits"

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
xcm_param = 'Temperature'
xcm_units = 'keV'


plot_patches(root, binmap, xcm_id, 
        out=out, out_title=out_title,
        title_font_size=title_font_size, label_font_size=label_font_size,
        xcm_param=xcm_param, xcm_units=xcm_units,
        xaxis_label=xaxis_label, yaxis_label=yaxis_label, palette='coolwarm')


