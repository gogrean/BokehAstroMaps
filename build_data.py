from bokeh.plotting import ColumnDataSource

def BuildDataSource(dictionary,cat):
    source = ColumnDataSource(
        data = dict(
            x = dictionary[cat]['RA'],
            y = dictionary[cat]['DEC'],
            cluster = dictionary[cat]['CLUSTER'],
            z = dictionary[cat]['REDSHIFT'],
            lx = dictionary[cat]['0.1-2.4 keV X-ray Luminosity (x 1E+44 erg/s)'],
            lx_err = dictionary[cat]['LX_err'],
            pow = dictionary[cat]['1.4 GHz Radio Power (x 1E+24 W/Hz)'],
            pow_err = dictionary[cat]['P14_err'],
            y500 = dictionary[cat]['SZ'],
            y500_err = dictionary[cat]['SZ_err']
        )
    )
    return source

def BuildTooltips():
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
    return tooltips0, extra_tooltips
