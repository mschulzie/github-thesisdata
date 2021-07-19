import warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import netCDF4
import helperlies as mway
import wrf
import string
from Python.modeloutput.input.zuordnung import soils, landuse
import importlib

#%%
path,save = mway.gimmedirs()
fe_name = 'DUSTSOILFE'
soil_name = 'ISLTYP'
src_name = 'DUSTSOURCE'
lu_name  = 'LU_INDEX'
veg_name  = 'IVGTYP'
data = warfy.Warfy()
data.load_var([fe_name,soil_name,src_name,lu_name,veg_name])
fe = data.get_var(fe_name).isel(time=0,dustbin_dim=0)
soil = data.get_var(soil_name).isel(time=0)
src = data.get_var(src_name).isel(time=0)
lu = data.get_var(lu_name).isel(time=0)
veg = data.get_var(veg_name).isel(time=0)

veg_levels = list(set(veg.values.flatten().tolist()))
veg_diff = (np.array(veg_levels)+np.diff(veg_levels+[20])/2)
veg_names = [landuse['Bez. Deutsch'][i-1] for i in veg_levels]
veg_colors = [landuse['colors'][i-1] for i in veg_levels]
soil_levels = list(set(soil.values.flatten().tolist()))
soil_diff = (np.array(soil_levels)+np.diff(soil_levels+[15])/2)
soil_names = [soils['Bez. Deutsch'][i-1] for i in soil_levels]
soil_colors = [soils['colors'][i-1] for i in soil_levels]
veg_levels = veg_levels + [20]
soil_levels=soil_levels + [15]

#%% PLOTTING
def format_ax(ax,abc):
    extent = [112.3,154.5,-44.5,-10]
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
    ax.add_feature(cfeature.STATES, zorder=2,lw=.5)
    ax.set_extent(extent, crs=crs.PlateCarree())
    ax.text(-.1,1,string.ascii_uppercase[abc],transform=ax.transAxes,
        weight='bold',fontsize=15)
    abc+=1
#%%
fig = plt.figure(figsize=(10,7))
gs = fig.add_gridspec(2,2,wspace=.7)
ax = fig.add_subplot(gs[0,0],projection=crs.Mercator(central_longitude=150.))
im_soil = soil.plot(ax=ax,transform=crs.PlateCarree(),levels=soil_levels,vmax=15,
    add_colorbar=False,colors=soil_colors)
cb = fig.colorbar(im_soil)
cb.set_ticks(soil_diff)
cb.set_ticklabels(soil_names)
cb.ax.tick_params(labelsize=8)
format_ax(ax,0)
ax.set_title('Vorherrschender Bodentyp')
ax2 = fig.add_subplot(gs[1,0],projection=crs.Mercator(central_longitude=150.))
im_veg = veg.plot(ax=ax2,transform=crs.PlateCarree(),levels=veg_levels,
    add_colorbar=False,colors=veg_colors)
cb2 = fig.colorbar(im_veg)
cb2.set_ticks(veg_diff)
cb2.set_ticklabels(veg_names)
cb2.ax.tick_params(labelsize=8)
format_ax(ax2,2)
ax2.set_title('Landnutzung/Vegetation')
ax3=fig.add_subplot(gs[0,1],projection=crs.Mercator(central_longitude=150.))
im_src = src.plot(ax=ax3,transform=crs.PlateCarree(),
    add_colorbar=False,levels=[0,1,2],colors=['#f5aaaa','#688f6b'])
format_ax(ax3,1)
ax3.add_feature(cfeature.OCEAN, zorder=2,fc='#a3caf7')
ax3.set_title('Staubquelle')
cb3 = fig.colorbar(im_src,shrink=0.5)
cb3.set_ticks([0.5,1.5])
cb3.set_ticklabels(['Nein','Ja'])
ax4 = fig.add_subplot(gs[3],projection=crs.Mercator(central_longitude=150.))
im_fe = fe.plot(ax=ax4,transform=crs.PlateCarree(),levels=10,
    add_colorbar=False)
format_ax(ax4,3)
ax4.add_feature(cfeature.OCEAN, zorder=2,fc='#a3caf7')
ax4.set_title('Anteil Eisen')
cb4 = fig.colorbar(im_fe)
ticks4= np.arange(0,0.045,0.005)
cb4.set_ticks(ticks4)
cb4.set_ticklabels(['{:.1f}%'.format(i*100) for i in ticks4])
fig.savefig('./Thesis/bilder/soil_type_iron.png',dpi=300,
    facecolor='white',bbox_inches='tight',pad_inches=0.01)
