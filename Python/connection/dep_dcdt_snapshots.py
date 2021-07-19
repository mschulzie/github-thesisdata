import numpy as np
import helperlies as mway
from matplotlib.colors import LogNorm, SymLogNorm
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import string

path = 'D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana.nc'
offset = 4
extend = 4
norm_std = True
percent_dev = False
minus_climate_mean = False
chl_max = 3
iron_min = 1e-6#iron.min().values
norm = SymLogNorm(2e-1,base=10,vmin=-chl_max,vmax=chl_max)
cbformat = '%.1f'
cbticks = [-3,-2,-1,-.5,-.2,-.1,0,.1,.2,.5,1,2,3]

add=''
chl_label = '\nVeränderung Chl-a in mg/m3 pro Tag'
iron = mway.import_iron_dep(landmask=True)[1:,...] # drop first timestep
iron = iron.coarsen(time=8,boundary='exact').mean(keep_attrs=True)
iron = iron.assign_coords(time=pd.date_range('2009-09-18','2009-09-29',freq='d'))
chl_raw = xr.open_dataset(path)['CHL']
if minus_climate_mean:
    path_cli = path[:-3]+'_climate.nc'
    chl_raw_cli = xr.open_dataset(path_cli)['CHL_mean']
    chl_raw.values -= chl_raw_cli.values
    add+='_climate_corr'
    chl_label+=' (Klima korrigiert)'

chl_diff = chl_raw.diff(dim='time')
start = pd.to_datetime(iron.time[0].values)+pd.DateOffset(days=offset)
stop = pd.to_datetime(iron.time[-1].values)+pd.DateOffset(days=offset+extend)
chl_diff = chl_diff.sel(time=slice(start,stop))
chl_diff = chl_diff.coarsen(lon=10,lat=10,boundary='trim').mean(keep_attrs=True)
iron_max = iron.max().values

if norm_std:
    chl_diff.values = chl_diff.values / chl_diff.values.std(axis=0)
    chl_label = '\nVeränderung Chl-a pro Tag (genormt mit Std.abw.)'
    chl_max= np.nanmax(abs(chl_diff.values))
    add+='_normalized'
    norm=None
    cbticks = np.arange(-4,5,1)
    cbformat='%d'

if percent_dev:
    chl_raw = chl_raw.sel(time=slice(start,stop))
    chl_raw = chl_raw.coarsen(lon=10,lat=10,boundary='trim').mean(keep_attrs=True)
    chl_diff.values = chl_diff.values / chl_raw.values * 100
    chl_label = '\nVeränderung Chl-a pro Tag in %'
    chl_max = 400
    add+='_in_percent'
    norm = SymLogNorm(50,base=10,vmin=-chl_max,vmax=chl_max)
    cbformat = '%d'
    cbticks = [-400,-200,-100,-50,-20,0,20,50,100,200,400]
#%% FORMAT AXES:
def format_ax(ax,text=None):
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=4)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=5)
    ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
    ax.set_title('')
    ax.set_xticks([])
    ax.set_xticklabels('')
    ax.set_xlabel('')
def letter_label(ax,i):
    ax.text(0., 1.02, string.ascii_uppercase[i], transform=ax.transAxes,
            size=20, weight='bold')
#%% PLOT

fig = plt.figure(figsize=(9,12))
gs = fig.add_gridspec(2,2,width_ratios=[30,1],hspace=0.05,wspace=0.1,
    height_ratios=[3,4])

gs1 = gs[0].subgridspec(3,4,hspace=0,wspace=0)
gs1_cb = gs[1]
gs2 = gs[2].subgridspec(4,4,hspace=0,wspace=0)
gs2_cb = gs[3]

for i,j in enumerate(gs1):
    ax = fig.add_subplot(gs1[i],projection=crs.Mercator(central_longitude=150.0))
    im1 = iron[i,...].plot(ax=ax,transform=crs.PlateCarree(),cmap='cool',
    add_colorbar=False,norm=LogNorm(vmin=iron_min,vmax=iron_max),levels=10)
    ax.text(112,-56,str(iron[i,...].time.values)[:10]
        ,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
    format_ax(ax)
    if i ==0:
        letter_label(ax,0)
for i,j in enumerate(gs2):
    ax = fig.add_subplot(gs2[i],projection=crs.Mercator(central_longitude=150.0))
    im2 = chl_diff[i,...].plot(ax=ax,transform=crs.PlateCarree(),cmap='RdBu_r',
    add_colorbar=False,norm=norm,vmin=-chl_max,vmax=chl_max)
    ax.text(112,-56,str(chl_diff[i,...].time.values)[:10]
        ,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
    format_ax(ax)
    if i ==0:
        letter_label(ax,1)
cb_ax1 = fig.add_subplot(gs1_cb)
cb_ax2 = fig.add_subplot(gs2_cb)
cb1 = fig.colorbar(im1,cax=cb_ax1)
cb2 = fig.colorbar(im2,cax=cb_ax2,format=cbformat)
cb2.set_ticks(cbticks)
cb1.set_label('Mittlerer Eiseneintrag in {:}'.format(iron.units))
cb2.set_label(chl_label)
2096/18900
plt.show()


fig.savefig('./Thesis/bilder/snapshot'+
    add+'.png',dpi=300,
    bbox_inches = 'tight',pad_inches = 0.01)
