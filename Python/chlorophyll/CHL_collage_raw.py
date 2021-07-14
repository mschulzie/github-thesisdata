import xarray as xr
import helperlies as mway
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm

ds = xr.open_mfdataset("D://thesisdata/plankton/marine_copernicus/2009_raw/*.nc")
ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
ds = ds['CHL']
extent = [110,179,-10,-57]
ds = ds.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
#%%
fig = plt.figure(figsize=(8,7))
gs = fig.add_gridspec(5,4,hspace=.05,wspace=.05,height_ratios=[8]*4+[1])

for i,time in enumerate(pd.date_range('2009-09-23','2009-10-08',freq='d')):
    dt = ds.sel(time=time).squeeze()
    ax = fig.add_subplot(gs[i], projection=crs.Mercator(central_longitude=150.0))
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
    im = dt.plot(
        ax=ax, cmap='viridis', add_colorbar=False,
        transform=crs.PlateCarree(), zorder=2,
        norm=LogNorm(vmin=0.1,vmax=3)
        )
    ax.set_extent(extent, crs=crs.PlateCarree())
    ax.set_title('')
    ax.text(112,-56,str(time)[:10]
        ,fontsize=8,transform = crs.PlateCarree(),
        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})

cbar_ax = fig.add_subplot(gs[16:20])
cb = fig.colorbar(im,orientation='horizontal',cax=cbar_ax,extend='max',
    shrink=.8,format='%.1f')
cb.set_ticks(np.array([0.1,0.2,0.5,1,2,3]))
cb.set_label('Chlorophyll-a in mg/m3')
plt.show()
fig.savefig('./Thesis/bilder/chl__raw_collage.png',
    dpi=200,facecolor='white',bbox_inches = 'tight',pad_inches = 0.01)
