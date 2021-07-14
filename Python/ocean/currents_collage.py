import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm,SymLogNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import pandas as pd
import helperlies as mway
import string

file = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_20m.nc'
ds_raw = xr.open_dataset(file)
for i in range(13):
    if i==0 or i==4:
        continue
    ds = ds_raw.isel(depth=i)
    depth = str(ds.depth.values)[:3]
    ds = ds.rename(longitude='lon',latitude='lat')
    ds = ds.sel(lon=slice(140,180),lat=slice(-48,-10))
    extent = [140,180,-48,-10]

    LON, LAT = np.meshgrid(ds.lon.values,ds.lat.values)

    box = [150,175,-40,-28]
    dt = ds.sel(time=slice('2009-09-18','2009-10-03'))
    u = dt['uo_mean'].squeeze()
    v = dt['vo_mean'].squeeze()
    s = np.sqrt(u.values**2 + v.values**2)
    speed = xr.DataArray(s,dims=u.dims,coords=u.coords,attrs=u.attrs)
    speed.attrs['long_name'] = 'sea water velocity'
    speed.attrs['standard_name'] = 'sea water velocity'

    def format_ax(ax):
        ax.coastlines(lw=.5, zorder=2)
        ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
        ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
        ax.set_extent(extent, crs=crs.PlateCarree())

    fig = plt.figure(figsize=(10,12))
    gs = fig.add_gridspec(5,4,height_ratios=[10,10,10,10,1],hspace=0)
    for i,time in enumerate(dt.time):
        ax = fig.add_subplot(gs[i],projection=crs.Mercator(central_longitude=150.))
        im = speed.sel(time=time).plot(ax=ax,transform=crs.PlateCarree(),cmap='jet',
             add_colorbar=False,vmin=0,vmax=.8,zorder=1,extend='max')
        ax.streamplot(LON,LAT,u.sel(time=time).values,v.sel(time=time).values,
            transform=crs.PlateCarree(),density=3,color='white',linewidth=.4,
            arrowsize=.5,zorder=4)
        format_ax(ax)
        ax.set_title(str(time.values)[:10])
    cax = fig.add_subplot(gs[4,:])
    cb = fig.colorbar(im,shrink=.9,extend='max',orientation='horizontal',cax=cax)
    cb.set_label('Strömungsgeschwindigkeit in m/s')
    fig.savefig('D://thesisdata/bilder/Python/currents/currents_collage_depth_'+
        '{:}m.png'.format(depth),dpi=300,
        facecolor='white',bbox_inches = 'tight',pad_inches = 0.01)
#plt.close()
