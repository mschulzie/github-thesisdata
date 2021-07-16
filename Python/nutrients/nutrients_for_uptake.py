import xarray as xr
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import string
ds2
path = 'D://thesisdata/nutrients/'
file = 'global-reanalysis-bio-001-029-monthly_1622729430962.nc'
ds = xr.open_dataset(path+file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(
    longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(110,180),lat=slice(-60,-10),time='2009-09-16')
#%%
file2 = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_20m.nc'
ds2 = xr.open_dataset(file2).isel(depth=0).drop('depth')
ds2 = ds2.assign_coords(longitude=(ds2.longitude % 360)).roll(
    longitude=(ds2.dims['longitude'] // 2), roll_coords=True)
ds2 = ds2.sel(time='2009-09-23')
ds2 = ds2.rename(longitude='lon',latitude='lat')
ds['T'] = ds2['thetao_mean']
ds['T'].attrs['units'] = '°C'
ds['MLD'] = ds2['mlotst_mean']
#%% FUNCTIONS
def format_ax(ax):
    extent = [110,179,-57,-10]
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
    ax.add_feature(cfeature.STATES, zorder=2,lw=.5)
    ax.set_extent(extent, crs=crs.PlateCarree())
def set_cmap(var,cmaps):
    try:
        cmap=cmaps[var]
    except KeyError:
        cmap='Greens'
    return cmap
def set_norm(var,norms):
    try:
        norm=norms[var]
    except KeyError:
        norm=None
    return norm
def set_vmin(var,vmins):
    try:
        vmin=vmins[var]
    except KeyError:
        vmin=None
    return vmin
def set_vmax(var,set_vmaxs):
    try:
        vmax=vmaxs[var]
    except KeyError:
        vmaxs=None
    return vmax
def set_level(var,level):
    try:
        levels=level[var]
    except KeyError:
        levels=10
    return levels
def set_title(var,titles):
    try:
        title=titles[var]
    except KeyError:
        title=''
    return title
#%% CHOOSE VARS AND PLOT!
vars = ['no3','po4','si','T','spco2','o2','MLD','ph','nppv']
ds['spco2']
fig = plt.figure(figsize=(10,8))
gs = fig.add_gridspec(3,3,hspace=0.05,wspace=0.15)
cmaps = {'no3':'YlGnBu','T':'coolwarm','po4':'OrRd','o2':'Blues',
    'ph':'PuOr','spco2':'Purples','MLD':'magma_r','si':'pink_r'}
norms = {'nppv':LogNorm(1e-1),'no3':LogNorm(1e-1),'po4':LogNorm(1e-1),
    'si':LogNorm(9e-1)}
vmins = {'T':5,'ph':8,'MLD':0}
vmaxs = {'T':25,'ph':8.2,'MLD':200,'si':15,'no3':20,'po4':1.5}
level = {'T':9,'ph':11,'MLD':11}
titles = {'spco2':r'CO$_2$ Partialdruck','o2':r'O$_2$ gelöst','MLD':'Mixed Layer Tiefe',
    'no3':'Nitrat','po4':'Phospat','T':'Wassertemperatur','si':'Silikat gelöst',
    'ph':'PH-Wert','nppv':'Primärproduktion'}

for i,var in enumerate(vars):
    if var=='fe':
        continue
    cmap = set_cmap(var,cmaps)
    norm = set_norm(var,norms)
    vmin = set_vmin(var,vmins)
    vmax = set_vmin(var,vmaxs)
    levels = set_level(var,level)
    ax = fig.add_subplot(gs[i],projection=crs.Mercator(central_longitude=150.))
    im = ds[var].plot(ax=ax,transform=crs.PlateCarree(),cmap=cmap,
        add_colorbar=False,norm=norm,vmin=vmin,levels=levels,vmax=vmax)
    cb = fig.colorbar(im,shrink=.8)
    cb.set_label(ds[var].attrs['units'])
    ax.set_title(set_title(var,titles))
    format_ax(ax)
    ax.text(-.1,1,string.ascii_uppercase[i],transform=ax.transAxes,
        weight='bold',fontsize=15)

fig.savefig('D://thesisdata/bilder/Python/nutrients/factors_collage.png'
    ,dpi=300,
    facecolor='white',bbox_inches = 'tight',pad_inches = 0.01)
