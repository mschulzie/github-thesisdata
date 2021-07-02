from warfy import Warfy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import helperlies as mway
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

path, savepath = mway.gimmedirs()
#%%
varname = 'DUSTLOAD'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]
data = Warfy()
data.load_var(var,file=path)
data.sum_vars(var,varname)
dust = data.get_var(varname)
dust_total = dust * mway.calc_qm(dust)
dust_time = dust_total.sum(dim=('lon','lat'))


fig = plt.figure(figsize=(12,3))
gs = fig.add_gridspec(1,2,wspace=.2,width_ratios=[6,4])
ax = fig.add_subplot(gs[0],projection=crs.Mercator(
    central_longitude=150.0))
im = dust.sel(time='2009-09-22T09').plot(ax=ax,norm=LogNorm(vmin=1,vmax=1e7),
    cmap='YlOrBr',levels=20,add_colorbar=False,
    transform=crs.PlateCarree(),extend='max')
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
ax.set_title('')
cb = fig.colorbar(im, shrink=.95)
cb.set_ticks(10**np.arange(0,8))
cb.set_label('Staubgehalt in µg/m2')
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    draw_labels=True,
    linewidth=.4, color='gray', linestyle='dotted',
    zorder=4)
gl.top_labels,gl.bottom_labels = False,True
gl.right_labels,gl.left_labels = False,True
gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

ax2 = fig.add_subplot(gs[1])
dust_time.plot(ax=ax2,color='#471f00')
ticks = pd.date_range('2009-09-18T00','2009-09-30T00',freq='24H')
ax2.set_xticks(ticks)
ax2.set_xlim(pd.to_datetime('2009-09-18T00'),pd.to_datetime('2009-09-30T00'))
ax2.grid(axis='x')
ax2.set_xlabel('')
ax2.set_ylabel('Staubgehalt in µg')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))# - %H UTC'))
plt.show()
fig.savefig('./Thesis/bilder/dustload_time.png',dpi=200,facecolor='white',
    bbox_inches = 'tight',pad_inches = 0.01)
