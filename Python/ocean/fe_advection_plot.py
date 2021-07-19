import xarray as xr
from matplotlib.colors import LogNorm, SymLogNorm
import numpy as np
import helperlies as mway
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import string

C = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_land_source_0_Nm.nc')
F = mway.import_iron_dep(landmask=True,extend=['2009-09-17T21','2009-10-05T00'])
F_sum = F.cumsum('time') * 60*60*3
F_sum.values = mway.ug_per_qm_to_nM(F_sum.values,z=10)
#C_1 = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_land_source_1_nM.nc')
#C_cd = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_cent_diff.nc')
#%%
def format_ax(ax):
    extent = [110,179,-57,-10]
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
    ax.add_feature(cfeature.STATES, fc='lightgrey', zorder=1,lw=.5)
    ax.set_extent(extent, crs=crs.PlateCarree())
    ax.set_title('')
#%%
cmap = mway.make_segmented_cmap('#ffffff','#009934')
cmap2 = mway.make_segmented_cmap('#9e0d52','#ffffff','#009934')

times = ['2009-09-18T00','2009-09-23T00','2009-09-27T00','2009-10-01T00','2009-10-05T00']
len(times)
time = '2009-09-23T00'
fig = plt.figure(figsize=(10,6))
gs = fig.add_gridspec(4,len(times)-1,height_ratios=[1,10,10,1],wspace=0.01)
for i,time in enumerate(times):
    if i==0:
        continue
    ax = fig.add_subplot(gs[1,i-1],projection=crs.Mercator(central_longitude=150.))
    im = C.sel(time=time).plot(ax=ax,cmap=cmap,norm=LogNorm(1e-5),extend='max',
        vmax=1,transform=crs.PlateCarree(),add_colorbar=False,levels=6)
    format_ax(ax)

    diff = (C.sel(time=time)-C.sel(time=times[i-1])
        -(F_sum.sel(time=time)-F_sum.sel(time=times[i-1])))
    ax2 = fig.add_subplot(gs[2,i-1],projection=crs.Mercator(central_longitude=150.))
    im2 = diff.plot(ax=ax2,cmap='RdBu',
        norm=SymLogNorm(1e-5,base=10),extend='both',
        vmax=1,transform=crs.PlateCarree(),add_colorbar=False,levels=10)
    format_ax(ax2)
    ax2.set_title(time)
    if i==1:
        ax.text(-.1, 0.5,r'$C_{Fe}$'+'\nin nM', transform=ax.transAxes,
                size=10,rotation=90,ha='center',va='center')
        ax2.text(-.1, 0.5,r'$\Delta C_{Fe}$ durch Transport'+'\nin nM', transform=ax2.transAxes,
                size=10,rotation=90,ha='center',va='center')
        ax.text(-.15, 1.05,string.ascii_uppercase[0], transform=ax.transAxes,
                size=20,weight='bold')
        ax2.text(-.15, 1.05,string.ascii_uppercase[1], transform=ax2.transAxes,
                size=20,weight='bold')
cax = fig.add_subplot(gs[0,:])
cb = fig.colorbar(im,cax=cax,orientation='horizontal')
cax.xaxis.set_ticks_position('top')
cax.xaxis.set_label_position('top')

cax2 = fig.add_subplot(gs[3,:])
cb2 = fig.colorbar(im2,cax=cax2,orientation='horizontal')


fig.savefig('D://thesisdata/bilder/Python/currents/iron_transport.png',dpi=200,
    bbox_inches = 'tight',pad_inches = 0.01)
