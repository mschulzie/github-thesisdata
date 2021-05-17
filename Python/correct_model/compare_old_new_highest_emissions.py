import wrf
import xarray as xr
import netCDF4
import numpy as np
import warfy as wh
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
savepath = 'D://thesisdata/'
#file = '/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00'
file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'
old_file = 'D://thesisdata/wrf_dust/01-2021/wrfout_d01_2009-09-18_00_00_00'
constvar = ['VEGFRA','ROUGH_COR','LAI']
timevar = ['uvmet','SMOIS_COR','UST','UST_T']
# only  SMOIS_COR, UST and UST_T variable in time!!
new = wh.Warfy()
old = wh.Warfy()
new.load_var(constvar,file=file)
new.load_var(timevar)
old.load_var(constvar,file=old_file)
old.load_var(timevar,file=old_file)

emis = ['DUST_EMIS_ACC'] * 5
emis = [emis[i]+''+str(i+1) for i in range(5)]
new.load_var(emis)
old.load_var(emis,file=old_file)
new.sum_vars(emis,'DUST_EMIS_ACC_SUM')
old.sum_vars(emis,'DUST_EMIS_ACC_SUM')
check = new.get_var('DUST_EMIS_ACC_SUM')

#%%
# Highest Emissions from original run:
hlon=[140.02089,140.50768,140.50768,140.99446,140.02089,140.02089,
    140.02089,140.99446,140.99446,139.04732,136.61339,138.07375,140.50768,
    129.3116,138.56053,142.45482,140.99446,138.07375,142.45482,141.48125]
hlat = ([-25.154457,-23.379456,-23.825523,-23.379456,
    -23.825523,-24.27005,-23.379456,-23.825523,
    -24.713036,-23.825523,-28.198704,-27.768837,
    -24.713036,-31.574299,-27.337261,-24.713036,
    -24.27005,-27.337261,-24.27005,-23.379456])

#%%
fig = plt.figure(figsize=(10,12),constrained_layout=True)
gs = fig.add_gridspec(5,2)

for i in range(10):
    ax = fig.add_subplot(gs[i])
    new.get_var('UST').sel(lon=hlon[i],lat=hlat[i]).plot(ax=ax,label='UST',
        color='lightblue',linestyle='-')
    new.get_var('UST_T').sel(lon=hlon[i],lat=hlat[i]).plot(ax=ax,
        label='UST_T_new',color='red',linestyle='-')
    (new.get_var('DUST_EMIS_ACC_SUM')/100).sel(lon=hlon[i],lat=hlat[i]).plot(
        ax=ax,label='DUST_EMIS_ACC_SUM / 100_new', color='green'
        ,linestyle='-')
    old.get_var('UST_T').sel(lon=hlon[i],lat=hlat[i]).plot(ax=ax,
        label='UST_T_old',color='darkred',linestyle='--')
    (old.get_var('DUST_EMIS_ACC_SUM')/100).sel(lon=hlon[i],lat=hlat[i]).plot(
        ax=ax,label='DUST_EMIS_ACC_SUM / 100_old', color='darkgreen'
        ,linestyle='--')

    ax.set_xticks([])
    ax.set_xlabel('')
    ax.legend(fontsize=4,loc='upper right')

#test.get_var('uvmet_speed').isel(lon=lo,lat=la).plot(label='wind')
#plt.legend()
fig.savefig(savepath+'UST_T_emssions.png',dpi=500)
plt.close()
#%%
area = [135,144,-21,-28]

fig = plt.figure(figsize=(10,12))
gs = fig.add_gridspec(len(constvar),2,wspace=0.05,hspace=0.01)
cmaps = ['Greens','jet','Greens']

new = new.sel(lon=slice(135,144),lat=slice(-28,-21))
old = old.sel(lon=slice(135,144),lat=slice(-28,-21))

row=0
for c in constvar:
    map = fig.add_subplot(gs[row,0], projection=crs.Mercator(central_longitude=150.0))
    cmap=cmaps.pop(0)
    im = map.pcolormesh(new.get_var(c).lon.values,new.get_var(c).lat.values,
        new.get_var(c).max('time').values, transform=crs.PlateCarree(),
        zorder=1,cmap=cmap)
    map.add_feature(cfeature.STATES,lw=.5, zorder=2,edgecolor='black')
    map.set_title(c+': '+new.get_var(c).attrs['description'] +
        ' in ' + new.get_var(c).attrs['units'])
    gl = map.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=1, color='grey', linestyle='dotted',
        zorder=6)
    cb = plt.colorbar(im,shrink=0.7,aspect=40)
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator([area[0]+0.1,area[1]-0.1])
    gl.ylocator = mticker.FixedLocator([area[2]-0.1,area[3]+0.1])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    for k in range(len(highest_lon)):
        if ((area[0]<hlon[k]<area[1])&
            (area[3]<hlat[k]<area[2])):
            map.text(highest_lon[k],highest_lat[k],str(k+1),transform=
                crs.PlateCarree(), ha='center',va='center',zorder=3,
                fontsize=8)
    map.set_extent(area,crs=crs.PlateCarree())

    map2 = fig.add_subplot(gs[row,1], projection=crs.Mercator(central_longitude=150.0))
    im2 = map2.pcolormesh(old.get_var(c).lon.values,old.get_var(c).lat.values,
        old.get_var(c).max('time').values, transform=crs.PlateCarree(),
        zorder=1,cmap=cmap)
    map2.add_feature(cfeature.STATES,lw=.5, zorder=2,edgecolor='black')
    map2.set_title(c+': '+old.get_var(c).attrs['description'] +
        ' in ' + old.get_var(c).attrs['units'])
    gl = map2.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=1, color='grey', linestyle='dotted',
        zorder=6)
    cb = plt.colorbar(im,shrink=0.7,aspect=40)
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator([area[0]+0.1,area[1]-0.1])
    gl.ylocator = mticker.FixedLocator([area[2]-0.1,area[3]+0.1])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    for k in range(len(highest_lon)):
        if ((area[0]<hlon[k]<area[1])&
            (area[3]<hlat[k]<area[2])):
            map2.text(highest_lon[k],highest_lat[k],str(k+1),transform=
                crs.PlateCarree(), ha='center',va='center',zorder=3,
                fontsize=8)
    map2.set_extent(area,crs=crs.PlateCarree())
    row += 1

fig.suptitle('CORRECTED constant values vs ORIGINAL')
plt.subplots_adjust(top=0.99,bottom=0.01)
plt.show()

fig.savefig('D://thesisdata/emission_controls_compare.png',dpi=500)
