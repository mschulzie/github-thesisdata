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

options = ['WETDEP_ACC_','GRASET_ACC_','DRYDEP_ACC_']
fig = plt.figure(figsize=(8,3.2))
gs = fig.add_gridspec(1,3,hspace=0.3,wspace=0.1)
savename = 'dust_deposition_vars'
cmap = 'YlGnBu'
count = 0
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
        zorder=1,cmap=cmap,extend='max',add_colorbar=False,
        levels=10,norm=LogNorm(vmin=1e-1,vmax=1e6))
    print(dep.max().values)
    ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
    total = (dep.values * mway.calc_qm(dep)).sum() *1e-15 # in thousand tons
    title = 'insg. {:.1f} tausend Tonnen'.format(total)
    ax.set_title(title,fontsize=10)
    ax.text(112,-56,sum_name
        ,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
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
    count +=1
cbar_d_ax = fig.add_axes([.13, 0.2, 0.75, 0.03])
cb_d = fig.colorbar(cont,orientation='horizontal',cax=cbar_d_ax,extend='max')
cb_d.set_label('Staubeintrag in µg/m2')
plt.show()
fig.savefig('D://thesisdata/bilder/Python/wrfout/Deposition/'+savename+'.png',
    dpi=200,facecolor='white', bbox_inches = 'tight',pad_inches = 0)

10.4+68.5+1587.2
