import warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm

wetdep = ['WETDEP_1','WETDEP_ACC_1','DUSTWDLOAD_1']
drydep = ['DRYDEP_1','DRYDEP_ACC_1']
graset = ['GRASET_ACC_1']
fedep = ['WETDEP_SOILFE_1', 'DRYDEP_SOILFE_1','DUST_SOILFEDRYDEP_ACC_1',
    'DUST_SOILFEWETDEP_ACC_1','GRASET_SOILFE_1','SOILFEWD_1',
    'SOILFEWDLOAD_1']
feconc = ['DUST_SOILFE_ACC_1','SOILFELOAD_1','SOILFE_1']

options = ['WETDEP_ACC_','GRASET_ACC_','DRYDEP_ACC_',
    'DUST_SOILFEWETDEP_ACC_','GRASET_SOILFE_','DUST_SOILFEDRYDEP_ACC_']
nrows = 2
ncols = 3
fig = plt.figure(figsize=(5*ncols,3.2*nrows))
gs = fig.add_gridspec(nrows,ncols,hspace=0.4)
count = 0
row = 0
col = 0
savename = 'several_deposition_vars'

for var in options:
    sum_name = var[:-1]
    if count == ncols:
        count = 0
        row+=1
    col = count
    var = [var]*5
    var = [var[i]+str(i+1) for i in range(5)]

    data = warfy.Warfy()
    data.load_var(var)
    data.sum_vars(var, sum_name)
    dep = data.get_var(sum_name)
    dep = dep.sum(dim='time',keep_attrs=True)
    dep.values = dep.values * 3 * 60 * 60 #/ 1000 # sekunde zu gesamt, ug zu mg
    dep.values[dep.values<0] = dep.values[dep.values<0] * -1
    #dep.attrs['units'] = 'mg/m2'
    ax = fig.add_subplot(gs[row,col], projection=crs.Mercator(
        central_longitude=150.0))

    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=2)

    cont = dep.plot(ax=ax,transform=crs.PlateCarree(),
        zorder=1,cmap='PuBuGn',alpha=1, extend='max',add_colorbar=False,
        levels=50,norm=LogNorm(vmin=1e-10))
        #,vmin = -10 ,vmax=4)

    cb = plt.colorbar(cont, shrink=.98)

    cb.set_label(dep.description+' in '+dep.units,fontsize=8)

    ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
    title = 'WRF - '+sum_name + ' Total ACC'
    ax.set_title(title,fontsize=10)
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
    count+=1

plt.show()
fig.savefig('D://thesisdata/bilder/Python/wrfout/Deposition/'+savename+'.png',dpi=500)
