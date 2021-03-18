import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import cftime
import seaborn as sns
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

# Änderung von haboob

gray = '#2f2d2f'
sns.set(
	context 	= 'paper', #notebook, talk
	style 		= 'ticks',
	palette 	= 'muted',
	color_codes = True,
	font 		= 'sans-serif',
	rc={
		'axes.edgecolor'	: gray
		,'text.color' 		: gray
		,'axes.labelcolor' 	: gray
		,'xtick.color' 		: gray
		,'ytick.color' 		: gray
		,'figure.figsize' 	: [8.3,5] # 8.3 is dina4 paper width
		,'text.usetex':False
		}
        )

ds = xr.open_dataset("D://thesisdata/plankton/GMIS_A_CHLA_09_2009.nc")
ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
ds = ds.Chl_a
ds = 10**ds
ds = ds.sel(lon=slice(110.3,189.7),lat=slice(-9.89,-57.06))
#ds = ds.where(ds>0)
ds.coords
ds.lon.max()

extent = [ds.lon.min(),ds.lon.max(),ds.lat.max(),ds.lat.min()]

sns.set_context('paper')

fig = plt.figure(dpi=200)
ax1 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree(central_longitude=180.0))
ax1.coastlines(lw=.5, zorder=5)
ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
levels1 = [0.1, 0.2, 0.5,1, 2,3]
levels = list(np.logspace(-1,np.log10(3),100))


im = ds.plot(
    ax=ax1, cmap='viridis', add_colorbar=False,
    levels=levels,
    transform=ccrs.PlateCarree(), zorder=2
    )
cb = plt.colorbar(im, pad=0.03, shrink=0.8, extend='neither')
cb.set_label(label=r'Chlorophyll-$\alpha$ Concentration (mg/m$^{3}$)')
cb.set_ticks(levels1)

ax1.set_extent(extent, crs=ccrs.PlateCarree())
gl = ax1.gridlines(
    crs=ccrs.PlateCarree(), draw_labels=True,
    linewidth=1, color='gray', linestyle='--'
    )
gl.top_labels = False
gl.right_labels = False
ax1.set_title('September 2009')
fig.savefig('Dein erste Bild.png', dpi = 500)
plt.show()


python -m pip list
