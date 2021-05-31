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
from xmca import xMCA
import matplotlib.dates as mdates


ds = xr.open_dataset("D://thesisdata/mixed_layer/2009/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1620410775145.nc")
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(40,280),lat=slice(-65,-32))
mn = ds['mlotst_mean']
std = ds['mlotst_std']
fig = plt.figure()
ax = fig.add_subplot(111)
mn = mn.mean(('lon','lat'))
std = std.mean(('lon','lat'))
ax.fill_between(mn.time.values,mn.values-std.values,mn.values+std.values,
    color='#0094ff',facecolor='#b0d9fb',label='Standardabweichung')
ax.plot(mn.time.values,mn.values,color='#0d4df0',label='Mittelwert')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
ax.tick_params(axis='x', labelrotation=45)
ax.set_title('MLD südl. Ozean')
ax.set_ylabel('MLD in m')
ax.set_xlim(pd.to_datetime('2009-08-01'),pd.to_datetime('2009-11-30'))
ax.legend()
ax.grid(axis='x')
fig.savefig('D://thesisdata/bilder/Python/mixed_layer/southern.png',bbox_inches='tight',
    dpi=200)
