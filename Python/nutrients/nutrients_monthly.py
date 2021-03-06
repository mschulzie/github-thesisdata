import xarray as xr
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

path = 'D://thesisdata/nutrients/'
file = 'global-reanalysis-bio-001-029-monthly_1622729430962.nc'
ds = xr.open_dataset(path+file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(
    longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')

ds = ds['fe'].sel(time='2009-09',lon=slice(110,189),lat=slice(-57,-10))
ds.values = ds.values*1e3
ds.attrs['units'] = 'nM' # nanomole per litre
#ds.plot(norm=LogNorm(vmax=0.001))

fig = plt.figure(figsize=(10,3))
gs = fig.add_gridspec(1,2,width_ratios = [5,5],wspace=.25)
ax = fig.add_subplot(gs[1])
n, bins, patches = ax.hist(ds.values.flatten(),bins=np.logspace(
    np.log10(ds.min()),np.log10(ds.max()),100),color='#004c5b',
    label='Histogramm\nRegion sh. links\nSep. 2009')
start = bins[np.argmax(n)]
end = bins[np.argmax(n)+1]
ax.set_xscale('log')
#ax.set_xlabel('Eisenkonzentration in '+ds.attrs['units'])
ax.set_ylabel('Anzahl der Gitterzellen')
ax.plot([start,start],[0,2800],'r--',lw=.8)
ax.plot([end,end],[0,2800],'r--',lw=.8)
ax.text(start,2500,'von ca. {:.2} '.format(start),ha='right')
ax.text(end,2500,' bis {:.2} nM'.format(end),ha='left')
ax.legend(loc=5,fontsize=8)

ax2 = fig.add_subplot(gs[0], projection=crs.Mercator(
    central_longitude=150.0))
ax2.coastlines(lw=.5, zorder=5)
ax2.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax2.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax2.add_feature(cfeature.STATES,lw=.2, zorder=2)

cont = ds.plot(ax=ax2,transform=crs.PlateCarree(),
    zorder=1,cmap='cividis',extend='neither',add_colorbar=False,
    norm=LogNorm(vmin=1e-3,vmax=10),levels=[1e-3,5e-3,1e-2,5e-2,1e-1,5e-1,
    1,10])
    #,vmin = -10 ,vmax=4)
cb = plt.colorbar(cont, shrink=.98)
cb.set_ticks([1e-3,1e-2,1e-1,1,10])
#cb.set_label('Eisenkonzentration in '+ds.attrs['units'],fontsize=8)

ax2.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
ax2.set_title('Eisenkonzentration in '+ds.attrs['units'],fontsize=10)
gl = ax2.gridlines(
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

fig.savefig('D://thesisdata/bilder/Python/nutrients/nutrient_iron.png',dpi=200,facecolor='white',
bbox_inches = 'tight',pad_inches = 0.01)

#%%
