import xarray as xr
import helperlies as mway
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

ds = xr.open_dataset("D://thesisdata/plankton/monthly/2007_2020_GMIS_A_CHLA_Australia.nc")
ds = ds['Chl_a']
ds = ds.sel(time='2009-10-01')
ds.shape
#ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
ds = 10**ds
#ds = ds.where(ds>0)


extent = [ds.lon.min(),ds.lon.max(),ds.lat.min(),ds.lat.max()]

sns.set_context('paper')

fig = plt.figure(dpi=200)
ax1 = fig.add_subplot(1,1,1, projection=ccrs.Mercator(central_longitude=150.0))
ax1.coastlines(lw=.5, zorder=5)
ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
levels1 = [0.1, 0.2, 0.5,1, 2,3]
levels = list(np.logspace(-1,np.log10(3),100))

ds.coords
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
ax1.set_title('Oktober 2009')
fig.savefig('Dein erste Bild.png', dpi = 500)
plt.show()
