from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
from cartopy.feature import NaturalEarthFeature

from wrf import (to_np, getvar, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

ncfile = Dataset("D://thesisdata/wrf_dust/neu Sven/wrfout_d01_2009-09-18_00_00_00")
varname = "DUST_SOILFEDRYDEP_ACC_1"


#i = 40
for i in range(ncfile.dimensions['Time'].size): # dann plt.show() rausnehmen

    var = getvar(ncfile,varname, timeidx=i)
    lats, lons = latlon_coords(var)
    # Get the cartopy mapping object
    cart_proj = get_cartopy(var)

    fig = plt.figure(figsize=(12,6))
    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
                                 facecolor="none",
                                 name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    # Make the contour outlines and filled contours for the smoothed sea level
    # pressure.
    plt.contourf(to_np(lons), to_np(lats), to_np(var),
                 transform=crs.PlateCarree(),
                 cmap=get_cmap("viridis"))
    # Add a color bar
    plt.colorbar(ax=ax, shrink=.98, label=(var.description+' in '+var.units))

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(var))
    ax.set_ylim(cartopy_ylim(var))

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")

    plt.title(str(var.coords['Time'].values)[:13])

    fig.savefig(
                'D://thesisdata/bilder/Python/wrfout/'+varname+'/'
                +str(var.coords['Time'].values)[:13]+'.png', dpi = 300
                )
    plt.close()
    #plt.show()

#SHAO's Variablenvorschläge:
#
#Wetter
# 1: 4-D Variablen, P, T, U, V, um Wetter darzustellen
#
# Dust in Atmosphäre
# 2: DUST_ACC_1 ... 5
#
# Dust Deposition und Emission und Load
# 3: 3-D Variablen DUSTLOAD_ACC1 ... 5
# 4: EDUST1 ... 5, DRYDEP_ACC1 ... 5, WETDEP_ACC1 ... 5
# 5: GRASET_ACC1 ... 5
#
# Danach analysieren wir die Fe Größen
# 6: DUST_SOILFE***_ACC1 ... 5.
