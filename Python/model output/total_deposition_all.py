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

options = ['WETDEP_ACC_','GRASET_ACC_','DRYDEP_ACC_',
    'DUST_SOILFEWETDEP_ACC_','DUST_SOILFEGRASET_ACC_','DUST_SOILFEDRYDEP_ACC_']
nrows = 2
ncols = 3
fig = plt.figure(figsize=(4*ncols,3.2*nrows))
gs = fig.add_gridspec(nrows,ncols,hspace=0.3,wspace=0.1)
count = 0
savename = 'several_deposition_vars'
cmaps = ['YlGnBu','PuRd','YlOrBr','YlGnBu','PuRd','YlOrBr']

for var in options:
    sum_name = var[:-1]
    var = [var]*5
    var = [var[i]+str(i+1) for i in range(5)]

    data = warfy.Warfy()
    data.load_var(var)
    data.sum_vars(var, sum_name)
    dep = data.get_var(sum_name)
    dep.values = dep.values * 3 * 60 * 60 #acc over 3h
    dep = dep.sum(dim='time',keep_attrs=True)
    dep.values[dep.values<0] = dep.values[dep.values<0] * -1
    #dep.attrs['units'] = 'mg/m2'
    ax = fig.add_subplot(gs[count], projection=crs.Mercator(
        central_longitude=150.0))

    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=2)

    cont = dep.plot(ax=ax,transform=crs.PlateCarree(),
        zorder=1,cmap=cmaps[count],alpha=1, extend='max',add_colorbar=False,
        levels=10,norm=LogNorm(vmin=1e-11))
        #,vmin = -10 ,vmax=4)

    cb = plt.colorbar(cont, shrink=.98)

    #cb.set_label(r'Total deposition in $\mu$g/m$^2$',fontsize=8)

    ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
    total = (dep.values * mway.calc_qm(dep)).sum() *1e-15 # in thousand tons
    title = sum_name +r' in $\mu$g/m$^2$'+'\n(insg. {:.1f} tausend Tonnen)'.format(total)
    ax.set_title(title,fontsize=10)
    #ax.set_ylim(wrf.cartopy_ylim(var))
    gl = ax.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=.2, color='gray', linestyle='dotted',
        zorder=4)
    gl.top_labels,gl.bottom_labels = False,False
    gl.right_labels,gl.left_labels = False,False
    gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
    gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    count+=1

plt.show()
fig.savefig('D://thesisdata/bilder/Python/wrfout/Deposition/'+savename+'.png',
    dpi=500)
