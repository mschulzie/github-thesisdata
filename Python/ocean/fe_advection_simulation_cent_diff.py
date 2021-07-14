import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm,SymLogNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import pandas as pd
import helperlies as mway
import importlib
#%% SETTINGS:
z_0 = 10 # thickness of ocean iron mixing
source = 0 #SET arbitrary Fe concentration in nM for terrestric areas
#%%
file = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1622467797293.nc'
ds = xr.open_dataset(file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(110,189),lat=slice(-57,-9),time=slice('2009-09-18','2009-10-15'))
ds = ds.drop('depth')
mask = xr.open_dataset('D://thesisdata/wrf_dust/land_and_coast_mask.nc')
landmask = mask['land']
#%%
iron_raw = mway.import_iron_dep(extend=['2009-09-17T21','2009-10-05T00'])
iron_raw =iron_raw.fillna(0)
lon_dist, lat_dist = mway.grid_distances(iron_raw)
uv = ds.interp(coords=iron_raw.coords)
u = uv['uo_mean'].fillna(0).squeeze().values
v = uv['vo_mean'].fillna(0).squeeze().values
dx = np.zeros((138,124,164))
dy = np.zeros((138,124,164))
dx[:,...] = lon_dist.values
dy[:,...] = lat_dist.values
dt = 60*60*3 # in sekunden
#Convert Iron ug/m2/s to nM/s:
iron = mway.ug_per_qm_to_nM(iron_raw.values,z=z_0)

#%%
#LAND AS SOURCE OF IRON?
C = np.zeros((139,124,164)) # Allocate Grid für Fe_conc in nM
if source > 0:
    C[0,landmask==1] = source

for t in range(1,139):
    for i in range(1,123):
        for j in range(1,163):
            C[t,i,j] =  C[t-1,i,j] + dt * iron[t-1,i,j]
            if any([landmask[i,j],landmask[i,j+1],landmask[i,j-1]]):
                pass
            else:
                C[t,i,j] -= u[t-1,i,j] * dt/2/dx[t-1,i,j]*(C[t-1,i,j+1]-C[t-1,i,j-1])
            if any([landmask[i,j],landmask[i+1,j],landmask[i-1,j]]):
                pass
            else:
                C[t,i,j] -= v[t-1,i,j] * dt/2/dy[t-1,i,j]*(C[t-1,i+1,j]-C[t-1,i-1,j])
    print('timestep {:} finished'.format(t))
    if source > 0:
        C[t,landmask==1] = source

print('Maximum CFL is {:.2f}'.format(dt/dx.min() * abs(v).max()))
C_Fe = xr.DataArray(C,dims=iron_raw.dims,
    coords={'lon':iron_raw.lon.values,'lat':iron_raw.lat.values,
    'time':pd.date_range('2009-09-17T18','2009-10-05T00',freq='3h')})
C_Fe = C_Fe.where(landmask==0)
print('Maximum C_Fe is {:.2f}'.format(np.nanmax(C_Fe.values)))

C_Fe.to_netcdf('D://thesisdata/wrf_dust/fe_dep_advection_cent_diff.nc')
