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
ds = xr.open_dataset('D://thesisdata/weather_stuff/uv_t_msl_tp_slh.nc')
ds
ds = ds['tp']
time1=slice('2009-09-22T01','2009-09-22T12')
time2=slice('2009-09-22T13','2009-09-23T00')
time3=slice('2009-09-23T01','2009-09-24T00')
times = [time1,time2,time3]
tp = [None]*3

for i in range(len(times)):
    tp[i] = ds.sel(time=times[i]).sum(dim='time')
    times[i] = times[i].start[8:]+' bis '+times[i].stop[8:] + ' UTC'
    i+=1
#%%

fig = plt.figure(figsize=(12,3.5))
gs = fig.add_gridspec(1,len(times),hspace=0.4,wspace=0.01)

for i in range(len(times)):
    ax = fig.add_subplot(gs[i], projection=crs.Mercator(
        central_longitude=150.0))

    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=1)

    scale = 10
    levels = np.arange(10,90,10).tolist()
    levels.insert(0,1)
    LON, LAT = np.meshgrid(tp[i].longitude.values, tp[i].latitude.values)
    cont = ax.contourf(LON,LAT,tp[i]*1000, transform=crs.PlateCarree(),
        zorder=1,cmap='Blues',alpha=1,levels=levels,vmin=1)
    ax.contour(LON,LAT,tp[i]*1000, transform=crs.PlateCarree(),
        zorder=1,colors='black',levels=levels,linewidths=.2)

    ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
    ax.set_title(times[i])
    #ax.set_ylim(wrf.cartopy_ylim(var))


# cities = mway.loadcities()
# for city in cities:
#     ax.text(cities[city][0]+.1,cities[city][1]+.1,
#         city,fontsize=2,
#         zorder=8,transform=crs.PlateCarree(),ha='left')
#     ax.plot(cities[city][0],cities[city][1],color='red',
#         zorder=7,transform=crs.PlateCarree(),
#         marker='o',markersize=.2)

cbar_ax = fig.add_axes([.91, 0.15, 0.01, 0.7])
cb = fig.colorbar(cont, format='%d',cax=cbar_ax)
cb.set_label('Kumulierter Tagesniederschlag in mm',fontsize=8)
plt.show()

fig.savefig('D://thesisdata/bilder/Python/era5/precipitation/collage.png',
dpi=500)
