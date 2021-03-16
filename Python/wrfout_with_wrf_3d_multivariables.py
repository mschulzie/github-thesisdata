from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature

from wrf import (to_np, getvar, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ALL_TIMES)

ncfile = Dataset("D://thesisdata/wrf_dust/neu Sven/wrfout_d01_2009-09-18_00_00_00")
varname = "DUST_ACC_1"
var = getvar(ncfile,varname, timeidx=ALL_TIMES)
lats, lons = latlon_coords(var)
cart_proj = get_cartopy(var)

zeitpunkt = '2009-09-24T00'
#for zeitpunkt in var.coords['Time'].values: # dann plt.show() rausnehmen

fig = plt.figure(figsize=(12,6))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
ax.add_feature(cfeature.STATES,lw=.2, zorder=3)
#levels = list(np.linspace(0,var.max(),100))
plt.contourf(to_np(lons), to_np(lats), to_np(var.sel(Time=zeitpunkt)),
             transform=crs.PlateCarree(),
             cmap=get_cmap("viridis"), zorder=7)
#cblevels = list(np.arange(0,1750e3,250e3))
cb=plt.colorbar(ax=ax, shrink=.98, label=(var.description+' in '+var.units))
#cb.set_ticks(cblevels)
ax.set_xlim(cartopy_xlim(var))
ax.set_ylim(cartopy_ylim(var))
# Add the gridlines
#ax.gridlines(color="black", linestyle="dotted")
gl = ax.gridlines(
    crs=crs.PlateCarree(), draw_labels=True,
    linewidth=1, color='gray', linestyle='dotted',
    xlocs=[120,135,150,165,180], zorder=6
    )
gl.top_labels = False
gl.right_labels = False

plt.title(str(zeitpunkt)[:13])

fig.savefig(
            'D://thesisdata/bilder/Python/wrfout/'+varname+'/'
            +str(zeitpunkt)[:13]+'.png', dpi = 300
            )
plt.show()
plt.close()

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
