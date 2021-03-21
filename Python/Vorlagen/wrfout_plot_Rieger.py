from netCDF4 import Dataset
from xmca.xarray import xMCA
import xarray as xr
import numpy as np
import marcowhereareyou as mway
import wrfhelper as wrfhelp
import wrf
wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)

rain,_,_,_,_ = wrfhelp.loadvar(wrffile,'RAIN')
# ds = wrf.getvar(wrffile,'RAINC',timeidx=wrf.ALL_TIMES)
rain = rain.rename({'Time':'time','west_east':'lon','south_north':'lat'}).drop('XTIME')
rain = rain.isel(lon=slice(0,143))
rain = rain.coarsen({'lon':2,'lat':2},boundary='trim').mean()


dust,_,_,_,_ = wrfhelp.loadvar(wrffile,'DUSTLOAD_')
# dust = wrf.getvar(wrffile,'RAINC',timeidx=wrf.ALL_TIMES)
dust.shape
dust = dust.rename({'Time':'time','west_east':'lon','south_north':'lat'}).drop('XTIME')
dust = dust.isel(lon=slice(0,143))
dust = dust.coarsen({'lon':2,'lat':2},boundary='trim').mean()


#%%
import cartopy.crs as ccrs

mca = xMCA(rain,np.log(dust+1))
mca.set_field_names('rain','dust')
mca.normalize()
mca.solve(complexify=True)
mca.plot(mode=2, orientation='vertical', threshold=.3, projection=ccrs.EqualEarth())
mca.explained_variance(50).cumsum().plot()

import copy as cp
rmca = cp.deepcopy(mca)
rmca.rotate(10)
rmca.plot(mode=5, threshold=.2, orientation='vertical')

(rmca.pcs(scaling='eigen')['left']/np.sqrt(mca._n_observations['left'])).sel(mode=10).plot()

import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure()
ax = fig.add_subplot(111)
pcs['right'].sel(mode=2).plot(ax=ax)
sns.despine(ax=ax, offset=10, trim=True)

pcs = rmca.pcs()
np.corrcoef(pcs['left'].sel(mode=10),pcs['right'].sel(mode=10))

mca._field_coords['left']['lon'] = np.linspace(110,179,71)
mca._field_coords['left']['lat'] = np.linspace(-57,-10,62)
mca._field_coords['right']['lon'] = np.linspace(110,179,71)
mca._field_coords['right']['lat'] = np.linspace(-57,-10,62)
