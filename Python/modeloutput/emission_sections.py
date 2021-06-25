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
import importlib
importlib.reload(mway)
path, savepath = mway.gimmedirs()
times = pd.date_range('2009-09-21T00','2009-09-29T00',freq='d')
varname = 'DUST_EMIS_ACC'
savename = 'Emission sections'
extent = [112,155,-10,-40]
county_extent = [138,144,-22,-26]
LEB_extent = [134.5,140.5,-26.5,-31]

var = [varname] * 5
var = [var[i]+''+str(i+1) for i in range(5)]
#%%
data = Warfy()
data.load_var(var)
data.sum_vars(var,varname)
emis = data.get_var(varname).sel(lon=slice(extent[0],extent[1])
    ,lat=slice(extent[3],extent[2]))
emis = emis.sel(time=slice('2009-09-18T00','2009-09-30T00'))
emis.values = emis.values * 60*60*3 *1e-12
emis.values = emis.values * mway.calc_qm(emis)
emis = emis.sum('time')
emis.attrs['description'] = 'Total dust emisson'
emis.attrs['units'] = 'Tonnen'
emis.sum()
#%%
county_sum = emis.sel(lon=slice(county_extent[0],county_extent[1]),
    lat=slice(county_extent[3],county_extent[2])).sum()
LEB_sum = emis.sel(lon=slice(LEB_extent[0],LEB_extent[1]),
    lat=slice(LEB_extent[3],LEB_extent[2])).sum()
maxvals = mway.argmax_array(emis,186)
(emis[mway.argmax_n(emis,6)]/emis.sum()).values
(mway.argmax_array(emis,42).sum()/emis.sum()).values
#%%
fig= plt.figure(figsize=(10,3))
width_ratios = [6,4]
height_ratios = [1,40,5]
gs = fig.add_gridspec(3,2,wspace=0.4,width_ratios=width_ratios,height_ratios=height_ratios)
ax = fig.add_subplot(gs[:,0], projection=crs.Mercator(central_longitude=150.0))
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
ax.add_feature(cfeature.OCEAN,fc='#d9e7fc')
im_e = maxvals.plot(ax=ax,transform=crs.PlateCarree(),
        cmap='winter',zorder=1,
        extend='max',norm=LogNorm(vmin=1),add_colorbar=False)
ax.set_title('{:,} Tonnen insgesamt'.format(int(emis.sum().values)).replace(',','.'))
ax.set_extent(extent,crs=crs.PlateCarree())
gl = ax.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=.2, color='gray', linestyle='dotted',
        zorder=4)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = mticker.FixedLocator(np.arange(110,160,5).tolist())
gl.ylocator = mticker.FixedLocator(np.arange(-45,-10,5).tolist())
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.plot(mway.box_to_plot(county_extent)[0],mway.box_to_plot(county_extent)[1],
    'red',transform=crs.PlateCarree(),zorder=3)
ax.plot(mway.box_to_plot(LEB_extent)[0],mway.box_to_plot(LEB_extent)[1],
    'purple',transform=crs.PlateCarree(),zorder=3)
transform = crs.PlateCarree()._as_mpl_transform(ax)
ax.annotate('{:,} Tonnen'.format(int(county_sum)).replace(',','.'),
            xy=(county_extent[1], county_extent[2]),
            xytext=(146,-20),
            arrowprops=dict(facecolor='red',edgecolor='red',
                            arrowstyle="simple"),
            xycoords=transform,
            ha='center', va='bottom')
ax.annotate('{:,} Tonnen'.format(int(LEB_sum)).replace(',','.'),
            xy=(LEB_extent[0], LEB_extent[3]),
            xytext=(130,-37),
            arrowprops=dict(facecolor='purple',edgecolor='purple',
                            arrowstyle="simple"),
            xycoords=transform,
            ha='center', va='bottom')
cb = plt.colorbar(im_e,shrink=.9)
cb.set_label('Emissionen in Tonnen')
ax2 = fig.add_subplot(gs[1,1])
p = np.cumsum(np.insert(np.sort(emis.values[emis.values!=0])[::-1],0,0))
ax2.plot(p,linewidth=3,color='#03257e')
xticks = np.array([1,6,20,42,80])
pticks = p[xticks]
pticks
ax2.set_xticks(xticks)
ax2.set_yticks(pticks)
ax2.set_title('Kumuliert')
ax2.grid()
ax2.set_ylim(0,emis.sum().values*1.1)
ax2.set_xlim(-2,100)
ax2.set_xlabel('Anzahl der Quellen mit höchsten Emissionen')
ax2.set_ylabel('Emission in Tonnen')
ax3 = ax2.twinx()
ax3.set_ylim(0,1.1)
ax3.set_ylabel('Anteil')
ax3.set_yticks(np.arange(0,1.1,0.1))
plt.show()
#fig.savefig('./Thesis/bilder/emission_sections.png',dpi=500)
