import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import pandas as pd
import helperlies as mway
import importlib
importlib.reload(mway)

file = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1622467797293.nc'
ds = xr.open_dataset(file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(140,180),lat=slice(-40,-10))
extent = [140,180,-40,-10]


#%%
r = 1 #how coarse?
LON, LAT = np.meshgrid(ds.lon.values[::r],ds.lat.values[::r])


dt = ds.sel(time=slice('2009-09-18','2009-10-02'))
u = dt['uo_mean'].squeeze().max('time')
v = dt['vo_mean'].squeeze().mean('time')
s = np.sqrt(u.values**2 + v.values**2)
u.values = u.values/s
v.values = v.values/s
speed = xr.DataArray(s,dims=u.dims,coords=u.coords,attrs=u.attrs)
speed.attrs['long_name'] = 'sea water velocity'
speed.attrs['standard_name'] = 'sea water velocity'

fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(111,projection=crs.Mercator(central_longitude=150.))
ax.coastlines(lw=.5, zorder=2)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
ax.set_extent(extent, crs=crs.PlateCarree())
# ax.quiver(LON,LAT,u.values[::r,::r],v.values[::r,::r],
#     transform=crs.PlateCarree(),zorder=2,color='#2ed725')
ax.streamplot(LON,LAT,u.values[::r,::r],v.values[::r,::r],
    transform=crs.PlateCarree(),density=4,color='white',linewidth=.2,
    arrowsize=.5)
im = speed.plot(ax=ax,transform=crs.PlateCarree(),cmap='cividis',
    add_colorbar=False,vmin=0,vmax=1,zorder=1)
cb = fig.colorbar(im,shrink=.8)
ax.set_title('u max v mean')
#fig.savefig('D://thesisdata/bilder/Python/currents/'+str(time)[:13]+'.png',dpi=200)
#plt.close()
