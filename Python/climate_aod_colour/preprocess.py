import xarray as xr
import numpy as np
#%%
path = 'D://thesisdata/plankton/cds_daily_2016-2020/'
file = '*.nc'

pl = xr.open_mfdataset(path+file)
pl = pl.assign_coords(lon=np.mod(pl['lon'],360)).sortby('lon')
pl = pl.sel(lon=slice(110,190),lat=slice(-9,-60))
pl.to_netcdf('./2016-2020_Australia.nc')#,engine='h5netcdf')
#%%
ds = xr.open_dataset('2016-2020_Australia.nc')

ds = ds['chlor_a']

ds.shape
