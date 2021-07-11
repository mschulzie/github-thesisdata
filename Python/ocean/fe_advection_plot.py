import xarray as xr
from matplotlib.colors import LogNorm, SymLogNorm
import numpy as np
import helperlies as mway
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature

C = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_land_source_0_nM.nc')
F = mway.import_iron_dep(landmask=True)
time = '2009-09-26T00'
F_sum = F.sel(time=slice('2009-09-18T00',time)).sum('time')*60*60*3
F_sum.values = mway.ug_per_qm_to_nM(F_sum.values,z=10) # convert to nanomole
diff = C.sel(time=time)-F_sum
#%%
def format_ax(ax):
    extent = [110,179,-57,-10]
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
    ax.add_feature(cfeature.STATES, fc='lightgrey', zorder=1,lw=.5)
    ax.set_extent(extent, crs=crs.PlateCarree())
#%%
cmap = 'Oranges'
fig = plt.figure(figsize=(20,8))
gs = fig.add_gridspec(1,3)
ax = fig.add_subplot(gs[0],projection=crs.Mercator(central_longitude=150.))
im = C.sel(time=time).plot(ax=ax,cmap=cmap,norm=LogNorm(1e-5),
    vmax=1,transform=crs.PlateCarree(),add_colorbar=False,levels=10)
cb = fig.colorbar(im, shrink=.8)
format_ax(ax)

ax2 = fig.add_subplot(gs[1],projection=crs.Mercator(central_longitude=150.))
im2 = diff.plot(ax=ax2,norm=LogNorm(1e-5),vmax=1,
    transform=crs.PlateCarree(),add_colorbar=False,cmap=cmap,levels=10)
cb2 = fig.colorbar(im2, shrink=.8)
im3 = (diff*-1).plot(ax=ax2,norm=LogNorm(1e-5),vmax=1,
    transform=crs.PlateCarree(),add_colorbar=False,cmap='Blues',levels=10)
cb3 = fig.colorbar(im3, shrink=.8)
cb.set_ticklabels([1e-5,1e-4,1e-3,1e-2,1e-1,1e0]*-1)
cb.get_ticks()
format_ax(ax2)

ax3 = fig.add_subplot(gs[2],projection=crs.Mercator(central_longitude=150.))
im3 = F_sum.plot(ax=ax3,norm=LogNorm(1e-5),vmax=1,
    transform=crs.PlateCarree(),add_colorbar=False,cmap=cmap,levels=10)
cb3 = fig.colorbar(im3, shrink=.8)

format_ax(ax3)
