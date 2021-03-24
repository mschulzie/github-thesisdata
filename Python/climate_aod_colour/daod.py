import xarray as xr
import numpy as np
import xmca
from xmca.xarray import xMCA
import cartopy.crs as crs
import matplotlib.pyplot as plt

path = 'D://thesisdata/daod/monthly/'
file = '2007_2020-C3S.._Australia.nc'

daod = xr.open_dataset(path+file)
daod = daod['D_AOD550']
daod = daod.sel(time=slice('2007-01','2017-12'))
daod = daod.transpose('time','lat','lon')
daod = daod.sel(lon=slice(110,179))
daod.sel(time='2007-05').plot()
daod.attrs['long_name']
#%%

pca = xMCA(daod)
pca.set_field_names(daod.attrs['long_name'])
pca.solve(complexify=False)

eigenvalues=pca.singular_values()
pcs = pca.pcs()
eofs = pca.eofs()

pca.plot(mode=1)
pca.save_plot(mode=4)
