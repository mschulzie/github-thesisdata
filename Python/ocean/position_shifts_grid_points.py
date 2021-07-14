import xarray as xr
import helperlies as mway
from matplotlib.colors import LogNorm, SymLogNorm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from warfy import Warfy
import cartopy.crs as crs
import cartopy.feature as cfeature
import string
#%% SETTINGS:
tau = np.arange(11)
time_currents_start = '2009-09-22' # must be -1 !!!!
#%% LONSHIFT, LATSHIFT:
def to_lats(dy):
    return 360*dy / (2*np.pi*6371000)
def to_lons(dx,breite):
    return 360*dx/(2*np.pi*6371000*np.cos(breite/360*2*np.pi))
def get_tau_position(u,v,tau,dt=(60*60*24)):
    """
    provide u,v for correct time!! (start time must be correct!!)
    """
    coords = {'tau':tau,'pos':['lat','lon'],'lat':u.lat.values,'lon':u.lon.values}
    dims = ['tau','pos','lat','lon']
    pos = np.zeros((len(tau),2,u.lat.size,u.lon.size))
    idx_pos = np.zeros((len(tau),2,u.lat.size,u.lon.size),dtype='int')
    pos[0,1],pos[0,0]=np.meshgrid(u.lon.values,u.lat.values)
    idx_pos[0,1],idx_pos[0,0]=np.meshgrid(np.arange(u.lon.size,dtype='int'),np.arange(u.lat.size,dtype='int'))
    for t in tau[1:]:
        print('tau = {:} started...'.format(t))
        for i in range(u.lat.size):
            for j in range(u.lon.size):
                idx_lat = idx_pos[t-1,0,i,j]
                idx_lon = idx_pos[t-1,1,i,j]
                pos[t,0,i,j] = pos[t-1,0,i,j] + to_lats(v.values[t,idx_lat,idx_lon]*dt)
                pos[t,1,i,j] = pos[t-1,1,i,j] + to_lons(u.values[t,idx_lat,idx_lon]*dt,pos[t-1,0,i,j])
                idx_pos[t,0,i,j] = int(abs(pos[t,0,i,j]-u.lat.values).argmin())
                idx_pos[t,1,i,j] = int(abs(pos[t,1,i,j]-u.lon.values).argmin())
    pos = xr.DataArray(pos,coords=coords,dims=dims)
    idx_pos = xr.DataArray(idx_pos,coords=coords,dims=dims)
    return pos, idx_pos
#%% PREPROCESS:
iron_raw = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_land_source_0_Nm.nc')
iron = iron_raw.sel(time=slice('2009-09-18T00','2009-10-02'))[::8]
file = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_1622467797293.nc'
ds = xr.open_dataset(file)
ds = ds.assign_coords(longitude=(ds.longitude % 360)).roll(longitude=(ds.dims['longitude'] // 2), roll_coords=True)
ds = ds.rename(longitude='lon',latitude='lat')
ds = ds.sel(lon=slice(110,189),lat=slice(-57,-9),time=slice('2009-09-18','2009-10-15'))
ds = ds.drop('depth')
ds = ds.sel(time=slice(time_currents_start,'2009-10-15'))
uv = ds.interp(coords=iron_raw.drop('time').coords)
u = uv['uo_mean'].fillna(0).squeeze()
v = uv['vo_mean'].fillna(0).squeeze()
positions,idx_pos = get_tau_position(u,v,tau)
ds = positions.to_dataset(name='positions')
ds['idx_pos'] = idx_pos
ds.to_netcdf('D://thesisdata/currents/position_shifts_starting_{:}+1day'.format(time_currents_start))
