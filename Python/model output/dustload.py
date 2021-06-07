from warfy import Warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import helperlies as mway

path, savepath = mway.gimmedirs()
times = pd.date_range('2009-09-21T00','2009-09-29T00',freq='d')
varname = 'DUSTLOAD_ACC'
savename = 'DUSTLOAD'
varname2 = 'EDUST'
savename2 = 'DUST_EMIS'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]
var2 = [varname2]*5
var2 = [var2[i]+''+str(i+1) for i in range(5)]

data = Warfy()
data.load_var(var)
data.load_var(var2)
data.sum_vars(var,varname)
data.sum_vars(var2,varname2)
dust = data.get_var(varname)
emis = data.get_var(varname2).sel(time=slice('2009-09-18T03','2009-09-30T00'))
emis.values = emis.values * 60*60*3 *1e-12
emis.values = emis.values * mway.calc_qm(emis)
emis = emis.coarsen(time=8,boundary='exact',keep_attrs=True,coord_func='max').sum()
emis.attrs['description'] = 'Total dust emisson'
emis.attrs['units'] = 'Tonnen'
emis.values[emis.values==0]= np.nan
emis.max()
#%%
fig= plt.figure(figsize=(10,10))
height_ratios=[3,3,3,2]
gs = fig.add_gridspec(4,3,hspace=0.05,wspace=0.05,height_ratios=height_ratios)
LON, LAT = np.meshgrid(emis.lon.values,emis.lat.values)

for i in range(len(times)):
    d = dust.sel(time=times[i])
    e = emis.sel(time=times[i])
    ax = fig.add_subplot(gs[i], projection=crs.Mercator(central_longitude=150.0))
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
    im_d = d.plot(ax=ax,transform=crs.PlateCarree(),
        norm=LogNorm(vmin=1,vmax=1e7),vmin=1,
        cmap='YlOrBr',zorder=1,add_colorbar=False)
    im_e = e.plot(ax=ax,transform=crs.PlateCarree(),
        cmap='winter',zorder=1,
        extend='max',norm=LogNorm(vmin=1,vmax=25e4),
        add_colorbar=False)
    ax.set_title('')
    ax.text(112,-56,str(times[i]),fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
    ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
    gl = ax.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=.2, color='gray', linestyle='dotted',
        zorder=4)
    if i not in [0,3,6]:
        gl.left_labels = False
    if i not in [6,7,8]:
        gl.bottom_labels = False
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
    gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

cbar_d_ax = fig.add_axes([.13, 0.2, 0.75, 0.03])
cb_d = fig.colorbar(im_d,orientation='horizontal',cax=cbar_d_ax,extend='max')
cb_d.set_label(r'Staub in Atmosphäre in $\mu$g/m$^{2}$')
cbar_e_ax = fig.add_axes([.13, 0.1, 0.75, 0.03])
cb_e = fig.colorbar(im_e,orientation='horizontal',cax=cbar_e_ax,extend='max')
cb_e.set_label('Gesamtemissionen des Vortags in Tonnen')
plt.show()
plt.tight_layout()
fig.savefig('./Thesis/bilder/dustload.png',dpi=500)
