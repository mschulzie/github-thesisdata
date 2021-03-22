import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import cftime
import seaborn as sns
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)
import os

ds = xr.open_dataset('D://thesisdata/weather_stuff/uv_t_msl_tp_slh.nc')
ds = ds['tp']
dt = ds[::3,...]
dt = dt[1:,...]
for t in reversed(range(1,7)):
    dt.values[t+1::7,...]=dt.values[t+1::7,...]-dt.values[t::7,...]

dt.shape

ds.sel(time='2009-09-23T00').plot()

ds.coords['longitude'].values

cbarlabel = ds.attrs['VARIABLE']+' in ' +ds.u.attrs['units']


ds = ds.sel(latitude=slice(-10,-57.), longitude=slice(110,179))
extent = [ds.longitude.values.min(),ds.longitude.values.max(),ds.latitude.values.min(),ds.latitude.values.max()]

sns.set_context('paper')

zeitliste = ds.time.values.tolist()
for zeit in zeitliste:
    fig = plt.figure(dpi=200)
    ax1 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    ax1.coastlines(lw=.5, zorder=5)
    ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
    ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
    dt = ds.sel(time=zeit)
    dt = dt.coarsen(longitude=3,latitude=3,boundary='trim').mean()
    LON, LAT = np.meshgrid(dt.longitude.values, dt.latitude.values)
    magnitude  = np.sqrt(np.square(dt.u.values[0]) + np.square(dt.v.values[0]))
    LAT
    im = ax1.quiver(
                LON, LAT,
                dt.u.values[0]/magnitude,dt.v.values[0]/magnitude,
                magnitude,
                transform=ccrs.PlateCarree(),
                scale=50, cmap = 'Reds'
                )
    fig.colorbar(im, extend='max', label=cbarlabel)

    ax1.set_extent(extent, crs=ccrs.PlateCarree())
    ax1.set_title(str(dt.time.values)[:10])

    fig.savefig(
                'C://Users/mschu/Documents/Studium/Bachelorarbeit/Python/pics/'
                +str(dt.time.values)[:10]+'.png', dpi = 500
                )
    plt.show()
