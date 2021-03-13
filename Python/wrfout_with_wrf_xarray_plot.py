from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import xarray as xr


from wrf import (to_np, getvar, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, ALL_TIMES)

ncfile = Dataset("D://thesisdata/wrf_dust/neu Sven/wrfout_d01_2009-09-18_00_00_00")
varname = "DUST_SOILFEDRYDEP_ACC_1"
var = getvar(ncfile,varname,timeidx=ALL_TIMES)
var = var.rename({"west_east": "lon", "south_north": "lat", "Time":"time"})
cart_proj = get_cartopy(var)

fig = plt.figure(dpi=200)
ax = fig.add_subplot(1,1,1, projection=cart_proj)
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
im = var.sel(time='2009-09-19T00').plot(ax=ax, cmap='viridis',
            transform=ccrs.PlateCarree())

# fig.savefig(
#             'D://thesisdata/bilder/Python/wrfout/'+varname+'/'
#             +str(var.coords['Time'].values)[:13]+'.png', dpi = 300
#             )
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
