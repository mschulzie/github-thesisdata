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
u = ds['u10']
v = ds['v10']
speed = np.sqrt(u**2+v**2) * 3.6 / 1.852 # in knots
ds.coords
#%% Plotting:
scale= 10
extent = [110,180,-57,-10]
fig = plt.figure(figsize=(8,7))
gs = fig.add_gridspec(5,4,hspace=.05,wspace=.05,height_ratios=[8]*4+[1])
LON, LAT = np.meshgrid(u.lon.values, u.lat.values)
for i,time in enumerate(pd.date_range('2009-09-29T20','2009-09-30T11',freq='1h')):
    dt = speed.sel(time=time).squeeze()
    dt_u = u.sel(time=time).squeeze()
    dt_v = v.sel(time=time).squeeze()
    ax = fig.add_subplot(gs[i], projection=crs.Mercator(central_longitude=150.0))
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
    im = dt.plot(
        ax=ax, cmap='jet', add_colorbar=False,
        transform=crs.PlateCarree(), zorder=2,
        vmax=40)
    vec = ax.quiver(LON[::scale,::scale], LAT[::scale,::scale],dt_u.values[::scale,::scale],dt_v.values[::scale,::scale],
        transform=crs.PlateCarree(), zorder = 2)
    ax.set_extent(extent, crs=crs.PlateCarree())
    ax.set_title('')
    ax.text(112,-56,str(time)[:13]
        ,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})

cbar_ax = fig.add_subplot(gs[16:20])
cb = fig.colorbar(im,orientation='horizontal',cax=cbar_ax,extend='max',
    shrink=.8,format='%.1f')
#cb.set_ticks(np.array([0.1,0.2,0.5,1,2,3]))
cb.set_label('10m Wind in Knoten')
plt.show()
fig.savefig('D://thesisdata/bilder/Python/era5/wind/wind_hourly_new.png',
    dpi=200,facecolor='white',bbox_inches = 'tight',pad_inches = 0.01)
