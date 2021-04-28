import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import os
import helperlies as mway

#convert time steps to those in WRF-output
sea = xr.open_mfdataset('D://thesisdata/sea_level/sea_level_2009/*.nc')
time='2009-09-23'
sea = sea['sla']
sea = sea.sel(time=time,longitude=slice(110,190),latitude=slice(-60,-10))
sea.values = sea.values*1000
#%%

fig = plt.figure(figsize=(5,3.2))
gs = fig.add_gridspec(1,1,hspace=0.4)
ax = fig.add_subplot(gs[0,0], projection=crs.Mercator(
    central_longitude=150.0))

ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=1)

cont = sea.plot(ax=ax,transform=crs.PlateCarree(),
    zorder=1,cmap='RdBu',alpha=1, extend='max',add_colorbar=False,
    vmax=100)

cb = plt.colorbar(cont, shrink=.98,format='%d')
cb.set_label('Sea level anomaly in mm',
    fontsize=8)

ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
ax.set_title(time+'- ERA-5')
#ax.set_ylim(wrf.cartopy_ylim(var))
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    draw_labels=True,
    linewidth=1, color='gray', linestyle='dotted',
    zorder=4)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# cities = mway.loadcities()
# for city in cities:
#     ax.text(cities[city][0]+.1,cities[city][1]+.1,
#         city,fontsize=2,
#         zorder=8,transform=crs.PlateCarree(),ha='left')
#     ax.plot(cities[city][0],cities[city][1],color='red',
#         zorder=7,transform=crs.PlateCarree(),
#         marker='o',markersize=.2)

fig.savefig('D://thesisdata/bilder/Python/era5/sla/'+time+'.png',
    dpi=500)
