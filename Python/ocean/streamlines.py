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
ds = ds.sel(lon=slice(140,180),lat=slice(-50,-25))
chl = xr.open_mfdataset("D://thesisdata/plankton/marine_copernicus/2009/*.nc")
chl = chl.assign_coords(lon=(chl.lon % 360)).roll(lon=(chl.dims['lon'] // 2), roll_coords=True)
chl = chl.sel(lon=slice(140,180),lat=slice(-25,-50))
chl = chl['CHL']
#%%
r = 1
extent = [ds.lon.min(),ds.lon.max(),ds.lat.min(),ds.lat.max()]
LON, LAT = np.meshgrid(ds.lon.values[::r],ds.lat.values[::r])

for time in pd.date_range('2009-10-01','2009-10-01',freq='d'):
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

    fig = plt.figure(figsize=(6,5))
    ax = fig.add_subplot(111,projection=ccrs.Mercator(central_longitude=150.))
    ax.coastlines(lw=.5, zorder=2)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=0.2, color='gray', linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    im = chla.plot(ax=ax,transform=ccrs.PlateCarree(),add_colorbar=False,
        vmax=1,extend='max',norm=LogNorm(),cmap='RdBu')
    cb = plt.colorbar(im,shrink=0.8,extend='max')
    cb.set_label('Chlorphyll-a Konzentration\n in '+chla.units)
    ax.streamplot(LON,LAT,u.values[::r,::r],v.values[::r,::r],
        transform=ccrs.PlateCarree(),density=1,color='purple',linewidth=2,
        arrowsize=.5)
    ax.set_title(str(time)[:13])
    fig.savefig('D://thesisdata/bilder/Python/currents/'+str(time)[:13]+'.png',dpi=300)
    #plt.close()
