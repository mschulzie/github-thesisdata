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
ds_raw = ds_raw.rename(longitude='lon',latitude='lat')
ds_raw = ds_raw.sel(lon=slice(140,180),lat=slice(-48,-10))
for i in range(13):
    ds = ds_raw.isel(depth=i)
    depth = str(ds.depth.values)[:3]
    extent = [140,180,-48,-10]

    LON, LAT = np.meshgrid(ds.lon.values,ds.lat.values)

    box = [150,175,-40,-28]
    dt = ds.sel(time=slice('2009-09-18','2009-10-02'))
    u = dt['uo_mean'].squeeze().mean('time')
    v = dt['vo_mean'].squeeze().mean('time')
    s = np.sqrt(u.values**2 + v.values**2)
    speed = xr.DataArray(s,dims=u.dims,coords=u.coords,attrs=u.attrs)
    speed.attrs['long_name'] = 'sea water velocity'
    speed.attrs['standard_name'] = 'sea water velocity'

    info = 'Mittel {:.2f} m/s'.format(
        speed.sel(lon=slice(box[0],box[1]),lat=slice(box[2],box[3])).mean().values)
    info2 = 'Max {:.2f} m/s'.format(
        speed.sel(lon=slice(box[0],box[1]),lat=slice(box[2],box[3])).max().values)

    #u.values = u.values/s


    # VORTICITY
    dx, dy = mway.grid_distances(u)
    dx = dx[:,1:] # first entry ist killed by diff()
    dy = dy[1:,:]
    vort = (v.diff('lon')/dx-u.diff('lat')/dy)

    # VORTICITY TIMESERIES
    # u_time = dt['uo_mean'].squeeze()
    # v_time = dt['vo_mean'].squeeze()
    # vort_time = (v_time.diff('lon')/dx-u_time.diff('lat')/dy)
    # for i in range(14):
    #     vort_time.diff('time').isel(time=i).plot(norm=SymLogNorm(1e-6,base=10))
    #     plt.show()
    # vort_time.sel(lon=slice(160,175),lat=slice(-48,-20)).mean(dim=('lon','lat')).plot()
    #

    def format_ax(ax):
        ax.coastlines(lw=.5, zorder=2)
        ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
        ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
        ax.set_extent(extent, crs=crs.PlateCarree())

    fig = plt.figure(figsize=(10,4))
    gs = fig.add_gridspec(1,2)
    ax = fig.add_subplot(gs[0],projection=crs.Mercator(central_longitude=150.))
    im = speed.plot(ax=ax,transform=crs.PlateCarree(),cmap='jet',
         add_colorbar=False,vmin=0,vmax=.8,zorder=1,extend='max')
    ax.streamplot(LON,LAT,u.values,v.values,
        transform=crs.PlateCarree(),density=3,color='white',linewidth=.4,
        arrowsize=.5,zorder=4)
    cb = fig.colorbar(im,shrink=.9,extend='max')
    cb.set_label('Str??mungsgeschwindigkeit in m/s')
    x = mway.box_to_plot(box)[0]
    y = mway.box_to_plot(box)[1]
    ax.plot(x,y,zorder=6,color='red',transform=crs.PlateCarree())
    ax.text(box[0]+1,box[2]+1,info,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha':1, 'pad': 1},zorder=7)
    format_ax(ax)
    ax.set_title('Mittlere Str??mung 18.09. bis 02.10.2009')
    ax.text(-0.1, 0.9, string.ascii_uppercase[0], transform=ax.transAxes,
            size=20, weight='bold')

    ax2 = fig.add_subplot(gs[1],projection=crs.Mercator(central_longitude=150.))
    im2 = vort.plot(ax=ax2,norm=SymLogNorm(3e-6,base=10),transform=crs.PlateCarree(),
        add_colorbar=False,cmap='RdYlGn_r')
    cb2 =fig.colorbar(im2,shrink=.9,extend='max')
    cb2.set_label('Vortizit??t in 1/s')
    ax2.set_title(r'Mittlere Vortizit??t $\zeta$')
    format_ax(ax2)
    ax2.text(-0.1, .9, string.ascii_uppercase[1], transform=ax2.transAxes,
            size=20, weight='bold')

    1.8e6/1 /(60*60*24)
    fig.savefig('D://thesisdata/bilder/Python/currents/currents_mean_{:}_m.png'.format(
        depth),dpi=200,bbox_inches = 'tight',pad_inches = 0.01)
    #plt.close()
