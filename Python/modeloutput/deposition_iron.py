import warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import helperlies as mway
import matplotlib.dates as mdates
import os
import pandas as pd

#tres = mway.nM_to_ug_per_qm(0.01,z=10) #treshold
tres = 5
# AREAS:
sections = {'Nordwest':[110,142,-10,-30],
    'Korall':[142,175,-10,-30],
    'Tasman':[145,175,-30,-45],
    'Süden':[110,145,-30,-45],
    'Südozean':[120,180,-45,-57],
    'Komplette Domäne':[110,179,-10,-57]}

#%%
land = warfy.Warfy()
land.load_var('LANDMASK')
landmask = land.get_var('LANDMASK').isel(time=0)

total = mway.import_iron_dep()
total_sum = total.sum(dim='time') * 60 * 60 * 3
total_tres=total_sum.where(total_sum>tres)
# %%
fig = plt.figure(figsize=(10,3))
gs = fig.add_gridspec(5,2,hspace=.2,width_ratios=[10,8])
ax = fig.add_subplot(gs[:,0], projection=crs.Mercator(
    central_longitude=150.0))
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3,alpha=.7)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
im = total_tres.plot(ax=ax,norm=LogNorm(),zorder=1,transform=crs.PlateCarree(),
    add_colorbar=False,cmap='plasma')
cb = plt.colorbar(im,shrink=.9)
cb.set_label(r'Totale Eisendeposition in (>5) $\mu$g/m$^2$',fontsize=8)
LON, LAT = np.meshgrid(total_sum.lon,total_sum.lat)
# CONTOUR PLOT
cs = ax.contour(LON,LAT,total_sum,transform=crs.PlateCarree(),zorder=5,
    levels=[0.1,1,5.6],colors='#464646',linewidths=.5)
ax.clabel(cs,cs.levels,inline=True,fontsize=6,fmt='%.1f',
    colors='#ff49b1',inline_spacing=.1)
#--
ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
ax.set_title('Ozean Summe {:5.0f}t'.format(
    (total_sum*mway.calc_qm(total)).sum(skipna=True).values*1e-12))
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    linewidth=.5, color='gray', linestyle='dotted',
    zorder=3)
#BOXES:
l = 1
for section in sections:
    if (section != 'Komplette Domäne'):
        ax.plot(mway.box_to_plot(sections[section])[0],
            mway.box_to_plot(sections[section])[1],
            'red',transform=crs.PlateCarree(),zorder=6,lw=1)
        ax.text(sections[section][0]+1,sections[section][3]+1,str(l),
            transform=crs.PlateCarree(),
            va='bottom',color='red',fontsize=8,zorder=6,
            bbox={'facecolor': 'white', 'alpha': 0.9, 'pad': 1})
        l+=1

#-----
gl.top_labels,gl.bottom_labels = False,True
gl.right_labels,gl.left_labels = False,True
gl.xlocator = mticker.FixedLocator([120,135,150,165,180,189])
gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50,-57])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# RIGHT plot
dep_ocean = total.where(landmask==0)*mway.calc_qm(total)*60*60*3*1e-12
k=0
for section in sections:
    if section!='Komplette Domäne':
        ax = fig.add_subplot(gs[k,1])
        dep_section = dep_ocean.sel(
            lon=slice(sections[section][0],sections[section][1]),
            lat=slice(sections[section][3],sections[section][2]))
        k+=1
        sum_dep = int(dep_section.sum(skipna=True).values)
        dep_section.sum(dim=('lat','lon'),skipna=True).plot(
            ax=ax,label='{:}. {:} {:}t'.format(k,section,sum_dep),
            color='#000170')
        ax.set_xticks(pd.date_range('2009-09-18T00','2009-09-30T00',freq='1d'))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        ax.tick_params(labelsize=8)

        ax.tick_params(axis='x', labelrotation=45)
        if k!=5:
            ax.set_xticklabels('')
        ax.set_xlabel('')
        ax.set_xlim(pd.to_datetime('2009-09-18T00'),pd.to_datetime('2009-09-30T00'))
        ax.legend(loc='upper left',fontsize=8)
        ax.grid(axis='x')
        if k==1:
            ax.set_title('Zeitreihen Depositionen (in Tonnen, letzte 3h)')

plt.show()
plt.tight_layout()
fig.savefig('./Thesis/bilder/total_iron.png',
    dpi=200,bbox_inches = 'tight',pad_inches = 0.01)
