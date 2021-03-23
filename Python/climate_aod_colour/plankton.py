import xarray as xr
import os
import pandas as pd
import numpy as np

file = '2007_2020_GMIS_A_CHLA_Australia.nc'
path = 'D://thesisdata/plankton/monthly/'

ds = xr.open_dataset(path+file)
ds = ds['Chl_a']

ds.sel(time='2009-10-01').plot()
