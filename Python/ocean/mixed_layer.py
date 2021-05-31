import xarray as xr
import helperlies as mway
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
from xmca import xMCA
import matplotlib.dates as mdates


ds = xr.open_dataset("D://thesisdata/mixed_layer/2009/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1620410775145.nc")
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lat=slice(-70,-10))
ds = ds['mlotst_mean']


#%%
sns.set_context('paper')
extent = [ds.lon.min(),ds.lon.max(),ds.lat.min(),ds.lat.max()]
for time in pd.date_range('2009-09-09','2009-10-31',freq='d'):

    dt = ds.sel(time=time).squeeze()

    fig = plt.figure(figsize=(10,3))
    ax1 = fig.add_subplot(1,1,1, projection=ccrs.Mercator(central_longitude=150.0))
    ax1.coastlines(lw=.5, zorder=5)
    ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
    ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)

    im = dt.plot(
        ax=ax1, cmap='viridis', add_colorbar=False,
        transform=ccrs.PlateCarree(), zorder=2,extend='max',
        levels=[0,10,50,100,200,300,400,500]
        )
    cb = plt.colorbar(im, pad=0.03, shrink=0.8)
    cb.set_label(label='mixed layer depth in m')

    ax1.set_extent(extent, crs=ccrs.PlateCarree())
    gl = ax1.gridlines(
        crs=ccrs.PlateCarree(), draw_labels=True,
        linewidth=0.2, color='gray', linestyle='--'
        )
    gl.top_labels = False
    gl.right_labels = False
    ax1.set_title(str(time)[:10]+' daily MLD')
    path = 'D://thesisdata/bilder/python/mixed_layer/'
    fig.savefig(path+str(time)[:10]+'.png', dpi = 500)
    plt.show()
