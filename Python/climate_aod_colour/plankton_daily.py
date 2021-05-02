import xarray as xr
import numpy as np
from xmca.xarray import xMCA
import pandas as pd
import helperlies as mway
import matplotlib.pyplot as plt

path = 'D://thesisdata/plankton/marine_copernicus/'
file = '2009_local.nc'
pl = xr.open_dataset(path+file)
pl = pl.sel(lon=slice(110,179),lat=slice(-10,-60))
pl = pl['CHL']
pl.coords
#%%
pl = pl.sel(time=slice('2009-08-01','2009-10-31'))
pl = pl.coarsen(lon=20,lat=20,boundary='trim').mean()
#pl = pl.interpolate_na(dim='time')

#%%
pca = xMCA(pl)
pca.normalize()
pca.set_field_names('CHL_A')
pca.solve(complexify=False)
eigenvalues=pca.singular_values()
pcs = pca.pcs()
eofs = pca.eofs()

pca.plot(mode=1)
pca.save_plot(mode=2,path='C://Users/mschu/Documents/Studium/Bachelorarbeit/BACHSEM/bilder')
#pca.save_analysis(path=path)
