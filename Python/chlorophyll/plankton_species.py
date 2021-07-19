import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm,SymLogNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import numpy as np
path = 'D://thesisdata/plankton/marine_copernicus/types/'
file = 'dataset-oc-glo-bio-multi-l4-pft_4km_monthly-rep_1626702842062.nc'
ds = xr.open_dataset(path+file)
# Kill all errors:
for var in ds:
    if '_error' in var:
        ds = ds.drop(var)
data = xr.DataArray(dims=['type','time','lat','lon'],
    coords={'type':['DIATO','PICO','DINO','HAPTO'],
        'time':ds.time,'lat':ds.lat,'lon':ds.lon})
for i,p in enumerate(data.type.values):
    data[i] = ds[p].values
time = '2009-10-01'
data = data.sel(time=time)
frac = 100*data/data.sum('type')
#%% FORMAT AXES:
def format_ax(ax,title=None):
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=4)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=5)
    ax.set_extent([110,179,-10,-57],crs=crs.PlateCarree())
    ax.set_title(title)
#%%
domtype = data.fillna(0).argmax('type').where(data.sum('type')>0)

fig=plt.figure(figsize=(12,3))
gs = fig.add_gridspec(1,2,width_ratios=[1,2],wspace=.15)
gs0 = gs[1].subgridspec(1,2,wspace=.05)
ax = fig.add_subplot(gs[0],projection=crs.Mercator(central_longitude=150.))
im = domtype.plot(ax=ax,transform=crs.PlateCarree(),levels=[0,1,2,3,4],
    add_colorbar=False,colors=['#0f16c7','#00ffc2','#ff0000','#bf50fa'])
cb=fig.colorbar(im,shrink=0.8,pad=0.01)
cb.set_ticks([0.5,1.5,2.5,3.5])
cb.set_ticklabels(['Kieselalgen','Picophyto','Dinophyta','Haptophyta'])
format_ax(ax,'Dominante Spezies')

ax2 = fig.add_subplot(gs0[0],projection=crs.Mercator(central_longitude=150.))
im2 = frac.sel(type='DIATO').plot(ax=ax2,transform=crs.PlateCarree(),
    add_colorbar=False,levels=11,cmap='magma',vmax=100)
cb2=fig.colorbar(im2,shrink=0.8,pad=0.01)
cb2.set_ticks(np.arange(0,110,10))
format_ax(ax2,'Anteil Kieselalgen in %')

ax3 = fig.add_subplot(gs0[1],projection=crs.Mercator(central_longitude=150.))
im3 = frac.sel(type='PICO').plot(ax=ax3,transform=crs.PlateCarree(),
    add_colorbar=False,levels=11,cmap='magma',vmax=100)
cb3=fig.colorbar(im2,shrink=0.8,pad=0.01)
cb3.set_ticks(np.arange(0,120,20))
format_ax(ax3,'Anteil Picophytoplankton in %')

fig.savefig('D://thesisdata/bilder/Python/plankton/dominant_diatom_pico_{:}.png'.format(time),
    dpi=200,bbox_inches='tight',pad_inches=0.01)
