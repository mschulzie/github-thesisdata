import warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import netCDF4
import helperlies as mway
import wrf
import importlib
importlib.reload(warfy)
#%%
path,save = mway.gimmedirs()
data = warfy.Warfy()
var = 'DUSTSOILFE'
fe
data.load_var(var)
fe = data.get_var(var)
fe_sum = fe.mean('dustbin_dim').isel(time=0)
fe_sum.plot()

#%%
