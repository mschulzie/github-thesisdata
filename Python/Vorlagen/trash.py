from warfy import Warfy
import xarray as xr
import numpy as np

wrf = Warfy()
wrf.load_var('LANDMASK')
land = wrf.get_var('LANDMASK')[0,...]
edge = np.zeros(land.shape)
for i in np.arange(0,163):
    for j in np.arange(0,123):
        if land.values[j+1,i]==1:
            edge[j,i]=1
        if land.values[j,i+1]==1:
            edge[j,i]=1
for i in np.arange(1,164)[::-1]:
    for j in np.arange(1,124)[::-1]:
        if land.values[j-1,i]==1:
            edge[j,i]=1
        if land.values[j,i-1]==1:
            edge[j,i]=1
for i in np.arange(163):
    for j in np.arange(124):
        if land.values[j,i]==1:
            edge[j,i]=1
        if land.values[j,i]==1:
            edge[j,i]=1

edges =xr.DataArray(edge-land.values,dims=land.dims,coords=land.coords)
land.attrs={}
edges.attrs={}
ds2 = land.to_dataset(name = 'land')
ds2['coast'] = edges
ds2.attrs
ds2.to_netcdf('D://thesisdata/wrf_dust/land_and_coast_mask.nc',engine='h5netcdf')
