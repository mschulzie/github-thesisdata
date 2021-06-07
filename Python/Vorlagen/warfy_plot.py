from warfy import Warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import helperlies as mway

path, savepath = mway.gimmedirs()
time = '2009-09-22T15'

varname = 'DUSTLOAD_ACC'
savename = 'DUSTLOAD'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]
var2 = ['PREC_ACC_C','PREC_ACC_NC']
data = Warfy()
data.load_var(var,file=path)
data.load_var(var2,file=path)
data.sum_vars(var,varname)
data.sum_vars(var2,'RAIN')
dust = data.get_var(varname)
rain = data.get_var('RAIN')
dust = dust.sel(time=time)
rain = rain.sel(time=time)

fig= plt.figure(figsize=(5,3.2))
gs = fig.add_gridspec(1,1,hspace=0.4)

ax = fig.add_subplot(gs[0,0], projection=crs.Mercator(
    central_longitude=150.0))
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)

# cont = dust.plot(ax=ax,transform=crs.PlateCarree(),
#     zorder=1,cmap='Reds',alpha=1,add_colorbar=False,
#     levels=50,norm=LogNorm(vmin=1e-10))
#
# cont2 = rain.plot(ax=ax, transform=crs.PlateCarree(),
#     zorder=2,cmap='Blues',alpha=1,add_colorbar=False,
#     levels=[1,6,14,24],extend='neither')

LON, LAT = np.meshgrid(dust.lon.values,dust.lat.values)
cont = ax.contourf(LON, LAT,dust.values,norm=LogNorm(vmin=1e-8),
    zorder=2,transform=crs.PlateCarree(),cmap='YlOrBr')
cont2 = ax.contourf(LON, LAT,rain.values,
    zorder=3,transform=crs.PlateCarree(),cmap='winter',
    alpha=.5,levels=[1,5,10,15,20,25])
cb = plt.colorbar(cont, shrink=.98)
cb2 = plt.colorbar(cont2,shrink=.8, orientation='horizontal')

cb.set_label('Ave soilFe load in ug/m2',fontsize=8)
cb2.set_label('ACC Precipitation last 3h',fontsize=6)

ax.set_title('WRF - '+varname+' - '+time,fontsize=8)
ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    draw_labels=True,
    linewidth=.2, color='gray', linestyle='dotted',
    zorder=4)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

plt.show()
#fig.savefig(savepath+savename+'.png',dpi=500)
