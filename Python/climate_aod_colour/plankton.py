import xarray as xr
import os
import pandas as pd
import numpy as np

file = '2007_2020_GMIS_A_CHLA.nc'
path = 'D://thesisdata/plankton/monthly/'

ds = xr.open_dataset(path+file)

ds = ds.assign_coords(lon=np.mod(ds['lon'], 360))
ds = ds.sortby('lon')
ds = ds.sel(lon=slice(110,190),lat=slice(-9,-60))

ds.to_netcdf(path+'Australia.nc')
