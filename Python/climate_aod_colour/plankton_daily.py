import xarray as xr
import numpy as np
from xmca.xarray import xMCA
import pandas as pd
import marcowhereareyou as mway

path = 'D://thesisdata/plankton/cds_daily_2009/'
file = '2009_08-11_Australia.nc'

pl = xr.open_dataset(path+file)
pl = pl['chlor_a']
pl = pl.sel(lon=slice(110,179))#,lat=slice(-30,-60))
mway.show_nan(pl)

#%%

pl = pl.coarsen(lon=20,lat=20,boundary='trim').mean()
pl = pl.interpolate_na(dim='time')
pl = np.log10(pl)
pl = pl.sel(time=slice('2009-09-01','2009-10-31'))

#%%
pca = xMCA(pl)
pca.normalize()
pca.set_field_names('log10(CHL_A)')
pca.solve(complexify=True)

eigenvalues=pca.singular_values()
pcs = pca.pcs()
eofs = pca.eofs()

pca.plot(mode=3,threshold=0.5)
#pca.save_plot(mode=5,path=path)
#pca.save_analysis(path=path)
