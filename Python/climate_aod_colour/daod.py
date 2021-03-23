import xarray as xr
import os
import pandas as pd
import numpy as np
from datetime import datetime

file = '2007_2020-C3S-L3_AEROSOL-AER_PRODUCTS-IASI-METOPA-IMARS-MONTHLY-v7.0ALL.nc'
path = 'D://thesisdata/daod/monthly/'

ds = xr.open_dataset(path+file)
ds = ds['D_AOD550']
ds.sel(time='2009-09-01').plot()
ds = ds.transpose()
