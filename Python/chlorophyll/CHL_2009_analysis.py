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
from matplotlib.colors import SymLogNorm, LogNorm
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

climate = xr.open_mfdataset("D://thesisdata/plankton/marine_copernicus/climatology/*.nc")
dawn = xr.open_mfdataset("D://thesisdata/plankton/marine_copernicus/2009/*.nc")
climate = climate.assign_coords(lon=(climate.lon % 360)).roll(lon=(climate.dims['lon'] // 2), roll_coords=True)
dawn = dawn.assign_coords(lon=(dawn.lon % 360)).roll(lon=(dawn.dims['lon'] // 2), roll_coords=True)
climate = climate.sel(lon=slice(80,250),lat=slice(-10,-70))
dawn = dawn.sel(lon=slice(80,250),lat=slice(-10,-70))
#%%
cli = climate['CHL_mean']
dev = climate['CHL_standard_deviation']
ano = dawn['CHL']
extent = [cli.lon.min(),cli.lon.max(),cli.lat.min(),cli.lat.max()]
sns.set_context('paper')
#%%
def exceed(cli_mean,cli_dev,data,month=9,day=23):
    time_cli = '1998-'+str(month).zfill(2)+'-'+str(day).zfill(2)
    time = '2009-'+str(month).zfill(2)+'-'+str(day).zfill(2)
    excess = data.sel(time=time).squeeze()-cli_mean.sel(time=time_cli).squeeze()
    excess = excess.where(abs(excess.values)>2*cli_dev.sel(time=time_cli).squeeze().values)
    return excess
#%%
for month in range(9,11):
    for day in range(1,31):
        time_cli = '1998-'+str(month).zfill(2)+'-'+str(day).zfill(2)
        time = '2009-'+str(month).zfill(2)+'-'+str(day).zfill(2)
        dt = exceed(cli,dev,ano,month=month,day=day)

        fig = plt.figure(figsize=(10,15))
        ax1 = fig.add_subplot(3,1,1, projection=ccrs.Mercator(central_longitude=150.0))
        ax1.coastlines(lw=.5, zorder=5)
        ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
        ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)

        im = dt.plot(
            ax=ax1, cmap='RdBu', add_colorbar=False,
            transform=ccrs.PlateCarree(), zorder=2,
            norm=SymLogNorm(0.01,base=10,vmin=-3,vmax=3))

        cb = plt.colorbar(im, pad=0.03, shrink=0.8, extend='neither')
        cb.set_label(label=r'Chlorophyll-$\alpha$ Concentration (mg/m$^{3}$)')
        ax1.set_extent(extent, crs=ccrs.PlateCarree())
        gl = ax1.gridlines(
            crs=ccrs.PlateCarree(), draw_labels=True,
            linewidth=0.2, color='gray', linestyle='--'
            )
        gl.top_labels = False
        gl.right_labels = False
        ax1.set_title(str(time)[5:10]+r' 2009 anomaly more than $2\sigma$')
        ax2 = fig.add_subplot(3,1,2, projection=ccrs.Mercator(central_longitude=150.0))
        ano.sel(time=time).squeeze().plot(
            ax=ax2,norm=LogNorm(vmax=1),cmap='RdBu', levels=20,
            transform=ccrs.PlateCarree())
        ax3 = fig.add_subplot(3,1,3, projection=ccrs.Mercator(central_longitude=150.0))
        dev.sel(time=time_cli).squeeze().plot(
            ax=ax3,norm=LogNorm(vmin=0.01,vmax=1.),cmap='RdBu',levels=20,
            transform=ccrs.PlateCarree())
        ax2.set_extent(extent, crs=ccrs.PlateCarree())
        ax3.set_extent(extent, crs=ccrs.PlateCarree())
        ax2.set_title(str(time)[5:10]+' 2009 absolute Werte')
        ax3.set_title(str(time)[5:10]+r' Klima Standardabw. $\sigma$')
        plt.show()
        path = 'D://thesisdata/bilder/python/chl_a/auswertung/'
        fig.savefig(path+str(time)[:10]+'.png', dpi = 500)
        plt.close()
