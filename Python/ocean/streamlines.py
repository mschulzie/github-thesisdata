import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

file = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1622467797293.nc'
ds = xr.open_dataset(file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(150,165),lat=slice(-40,-33))
chl = xr.open_mfdataset("D://thesisdata/plankton/marine_copernicus/2009/*.nc")
chl = chl.assign_coords(lon=(chl.lon % 360)).roll(lon=(chl.dims['lon'] // 2), roll_coords=True)
chl = chl.sel(lon=slice(150,165),lat=slice(-33,-40))
chl = chl['CHL']
#%%

extent = [ds.lon.min(),ds.lon.max(),ds.lat.min(),ds.lat.max()]
LON, LAT = np.meshgrid(ds.lon.values,ds.lat.values)

time = '2009-10-02'
dt = ds.sel(time=time)
chla = chl.sel(time=time)
u = dt['uo_mean'].squeeze()
v = dt['vo_mean'].squeeze()
s = np.sqrt(u.values**2 + v.values**2)
# u.values = u.values/s
# v.values = v.values/s
speed = xr.DataArray(s,dims=u.dims,coords=u.coords,attrs=u.attrs)
speed.attrs['long_name'] = 'sea water velocity'
speed.attrs['standard_name'] = 'sea water velocity'

fig = plt.figure(figsize=(4,3))
gs = fig.add_gridspec(2,1,height_ratios=[20,1])
ax = fig.add_subplot(gs[0],projection=ccrs.Mercator(central_longitude=150.))
ax.coastlines(lw=.5, zorder=2)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
ax.set_extent(extent, crs=ccrs.PlateCarree())
im = chla.plot(ax=ax,transform=ccrs.PlateCarree(),add_colorbar=False,
    vmax=3,extend='max',norm=LogNorm(),cmap='viridis')
ax.streamplot(LON,LAT,u.values,v.values,
    transform=ccrs.PlateCarree(),density=2,color='#f7e5fb',linewidth=1,
    arrowsize=.5)
ax.set_title(str(time)[:13])
cax = fig.add_subplot(gs[1])
cb = fig.colorbar(im,cax=cax,extend='max',orientation='horizontal',shrink=.1)
cb.set_label('Chlorphyll-a Konzentration in mg/m3')
cb.set_ticks([0.1,0.2,0.5,1,2,3])
fig.savefig('D://thesisdata/bilder/Python/currents/'+str(time)[:13]+'.png',dpi=200,
    bbox_inches='tight',pad_inches=0.01,facecolor='white')
#plt.close()
