import warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

wetdep = ['WETDEP_1','WETDEP_ACC_1','DUSTWDLOAD_1']
drydep = ['DRYDEP_1','DRYDEP_ACC_1']
graset = ['GRASET_ACC_1']
fedep = ['WETDEP_SOILFE_1', 'DRYDEP_SOILFE_1','DUST_SOILFEDRYDEP_ACC_1',
    'DUST_SOILFEWETDEP_ACC_1','GRASET_SOILFE_1','SOILFEWD_1',
    'SOILFEWDLOAD_1']
feconc = ['DUST_SOILFE_ACC_1','SOILFELOAD_1','SOILFE_1']

var = ['GRASET_SOILFE_']*5
var = [var[i]+str(i+1) for i in range(5)]
var
data = warfy.Warfy()
data.load_var(var)
sum_name = var[0][:-2]
data.sum_vars(var, sum_name)
dep = data.get_var(sum_name)
dep.attrs
dep = dep.sum(dim='time',keep_attrs=True)
dep.values = dep.values * 3 * 60 * 60 / 1000 # sekunde zu gesamt, ug zu mg
dep.attrs['units'] = 'mg/m2'
#dep.values = np.log10(dep.values)
#%%
fig = plt.figure(figsize=(5,3.2))
gs = fig.add_gridspec(1,1,hspace=0.4)
ax = fig.add_subplot(gs[0,0], projection=crs.Mercator(
    central_longitude=150.0))

ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=1)

cont = dep.plot(ax=ax,transform=crs.PlateCarree(),
    zorder=1,cmap='PuBuGn',alpha=1, extend='max',add_colorbar=False)
    #,vmin = -10 ,vmax=4)

cb = plt.colorbar(cont, shrink=.98)#,format='%d')
# ticks = np.array([-10.,-8.,-6.,-4.,-2.,0.,2.,4.])
# cb.set_ticks(ticks)
# cb.set_ticklabels(10**ticks)

cb.set_label(dep.description+' in '+dep.units,fontsize=8)

ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
ax.set_title('WRF - '+sum_name)
#ax.set_ylim(wrf.cartopy_ylim(var))
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
