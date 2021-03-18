from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature

import wrf

ncfile = Dataset("D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00")

varname = "DUSTLOAD_ACC_1"
var = wrf.getvar(ncfile,varname, timeidx=wrf.ALL_TIMES)
lats, lons = wrf.latlon_coords(var)
cart_proj = wrf.get_cartopy(var)

zeitpunkt = '2009-09-23T06'
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
plt.contourf(wrf.to_np(lons), wrf.to_np(lats),
            wrf.to_np(var.sel(Time=zeitpunkt)),
             transform=crs.PlateCarree(),
             cmap=get_cmap("viridis"), zorder=7)
#cblevels = list(np.arange(0,1750e3,250e3))
cb=plt.colorbar(ax=ax, shrink=.98, label=(var.description+' in '+var.units))
#cb.set_ticks(cblevels)
ax.set_xlim(wrf.cartopy_xlim(var))
ax.set_ylim(wrf.cartopy_ylim(var))
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
