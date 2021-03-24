import xarray as xr
import numpy as np
import xmca
from xmca.xarray import xMCA

file = '2007_2020_GMIS_A_CHLA_Australia.nc'
path = 'D://thesisdata/plankton/monthly/'

pl = xr.open_dataset(path+file)
pl = pl['Chl_a']
pl = pl.sel(time=slice('2007-05','2017-12'),lon=slice(110,179))
name = pl.attrs['long_name']
pl = pl.coarsen(lon=10,lat=10,boundary='trim').mean()
pl = pl.transpose('time','lat','lon')

#%%
pca = xMCA(pl)
pca.set_field_names(name)
pca.solve(complexify=False)

eigenvalues=pca.singular_values()
pcs = pca.pcs()
eofs = pca.eofs()

pca.plot(mode=1)
pca.save_plot(mode=4)
