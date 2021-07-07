import xarray as xr
import os


path = 'D://thesisdata/plankton/marine_copernicus/climatology/'
ds = xr.open_mfdataset(path+'*.nc')
ds=ds.drop('CHL_percentile_97')
ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
ds = ds.sel(lon=slice(109,190),lat=slice(-9,-60),
    time=slice('1998-09-01','1998-10-31'))
#ds.compute()

#%%
ds.to_netcdf('D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana_climate.nc',
    engine='h5netcdf')
