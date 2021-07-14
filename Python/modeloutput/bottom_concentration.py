from warfy import Warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import helperlies as mway

path, savepath = mway.gimmedirs()
times = pd.date_range('2009-09-18T00','2009-09-29T00',freq='d')
varname = 'DUST_ACC'
savename = 'DUST_bottom_conc'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]

data = Warfy()
data.load_var(var)
data.sum_vars(var,varname)
hohe = Warfy()
hohe.load_var('z')
#%%
z = hohe.get_var('z').sel(time='2009-09-23T00')#,lon=slice(150,152),lat=slice(-35,-33))
z0 = z.sel(zlevel=0)
z1 = z.sel(zlevel=1)
(z1-z0).plot()

dust = data.get_var(varname)
dust = dust.sel(zlevel=0)
#dust.sel(time='2009-09-23T00',lon=slice(150,152),lat=slice(-35,-33)).plot(norm=LogNorm())
#RAUM SYDNEY:
dust.sel(time=slice('2009-09-23T00','2009-09-23T00'),
    lon=slice(150,152),lat=slice(-35,-33)).max().values
