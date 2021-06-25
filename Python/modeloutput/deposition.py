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

#options = ['WETDEP_ACC','GRASET_ACC','DRYDEP_ACC']
options = ['DUST_SOILFEWETDEP_ACC','DUST_SOILFEGRASET_ACC','DUST_SOILFEDRYDEP_ACC']

wet_name= options[0]
gra_name= options[1]
dry_name= options[2]

tres = mway.nM_to_ug_per_qm(0.01,z=10) #treshold
# AREAS:
sections = {'Nordost':[110,140,-10,-30],
    'Korall':[140,165,-10,-30],
    'Tasman':[145,175,-30,-45],
    'Süden':[110,145,-30,-45],
    'Südozean':[120,180,-45,-57],
    'full':[110,179,-10,-57]}

#%%
liste = [wet_name,gra_name,dry_name]
j = 0
for var in liste:
    var = [var]*5
    var = [var[i]+'_'+str(i+1) for i in range(5)]
    liste[j] = var
    j+=1

wet = warfy.Warfy()
wet.load_var(liste[0])
wet.sum_vars(liste[0],wet_name)
wet = wet.get_var(wet_name)
gra = warfy.Warfy()
gra.load_var(liste[1])
gra.sum_vars(liste[1],gra_name)
gra = gra.get_var(gra_name)
dry = warfy.Warfy()
dry.load_var(liste[2])
dry.sum_vars(liste[2],dry_name)
dry = dry.get_var(dry_name)
land = warfy.Warfy()
land.load_var('LANDMASK')
landmask = land.get_var('LANDMASK').isel(time=0)


gra.values[gra.values<0] = gra.values[gra.values<0] * -1
dry.values[dry.values<0] = dry.values[dry.values<0] * -1

total = xr.DataArray(gra.values+wet.values+dry.values,
    coords=wet.coords,dims=wet.dims,attrs=wet.attrs)
total.attrs['description'] ='Total dust deposition rate all binsizes'
total_sum = total.sum(dim='time') * 60 * 60 * 3
total_tres=total_sum.where(total_sum>tres)
# %%
fig = plt.figure(figsize=(10,4))
gs = fig.add_gridspec(5,2,hspace=.2,width_ratios=[10,8])
ax = fig.add_subplot(gs[:,0], projection=crs.Mercator(
    central_longitude=150.0))
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3,alpha=.8)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
im = total_tres.plot(ax=ax,norm=LogNorm(),zorder=1,transform=crs.PlateCarree(),
    add_colorbar=False,cmap='plasma')
cb = plt.colorbar(im,shrink=.7)
cb.set_label(r'Totale Eisendeposition in $\mu$g/m$^2$',fontsize=8)
ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
ax.set_title('Insgesamt {:5.0f}t'.format(
    (total_sum*mway.calc_qm(total)).sum(skipna=True).values*1e-12))
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    linewidth=.5, color='gray', linestyle='dotted',
    zorder=3)
#BOXES:
l = 1
for section in sections:
    if (section != 'full'):
        ax.plot(mway.box_to_plot(sections[section])[0],
            mway.box_to_plot(sections[section])[1],
            'red',transform=crs.PlateCarree(),zorder=3,lw=1)
        ax.text(sections[section][0]+1,sections[section][3]+1,str(l),
            transform=crs.PlateCarree(),
            va='bottom',color='red',fontsize=8,zorder=6,
            bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
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
    if section!='full':
        ax = fig.add_subplot(gs[k,1])
        dep_section = dep_ocean.sel(
            lon=slice(sections[section][0],sections[section][1]),
            lat=slice(sections[section][3],sections[section][2]))
        k+=1
        sum_dep = int(dep_section.sum(skipna=True).values)
        dep_section.sum(dim=('lat','lon'),skipna=True).plot(
            ax=ax,label='{:}. {:} {:}t'.format(k,section,sum_dep),
            color='#3c3c3c')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
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
fig.savefig('D://thesisdata/bilder/Python/wrfout/Deposition/total_iron.png',
    dpi=300)
