import xarray as xr
import numpy as np
import xmca
from xmca.xarray import xMCA
import cartopy.crs as crs
import matplotlib.pyplot as plt

# test #

path = 'D://thesisdata/daod/monthly/'
file = '2007_2020-C3S.._Australia.nc'

daod = xr.open_dataset(path+file)
daod = daod['D_AOD550']
daod = daod.sel(time=slice('2007-01','2017-12'))
daod = daod.transpose('time','lat','lon')
daod = daod.sel(lon=slice(110,179))
daod.sel(time='2007-05').plot()

plfile = '2007_2020_GMIS_A_CHLA_Australia.nc'
plpath = 'D://thesisdata/plankton/monthly/'
#test#
pl = xr.open_dataset(plpath+plfile)
pl = pl['Chl_a']
pl = pl.sel(time=slice('2007-05','2017-12'),lon=slice(110,179))
name = pl.attrs['long_name']
pl = pl.coarsen(lon=10,lat=10,boundary='trim').mean()
pl = pl.transpose('time','lat','lon')
pl.sel(time='2007-05').plot()
#%%

mca = xMCA(daod,pl)
mca.set_field_names('Dust AOD 550nm','log10(Chl_a)')
mca.solve(complexify=True)

eigenvalues=mca.singular_values()
mcs = mca.pcs()
eofs = mca.eofs()

mca.plot(mode=1,orientation='vertical',threshold=0.3)
mca.save_plot(mode=5,path=path,threshold=0.3)
