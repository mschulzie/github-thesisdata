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
dcdt = True
dfdt = True
fe_log10 = False
chl_log10 = False
minus_climate_mean = False
# For cb norm scroll down!
shift = 14 # how many gridpoints left,right, up or down do find max. cov?


#%% Function needed:
def corr_tau(x,y,tau,lat_shift=np.array([0]),lon_shift=np.array([0])):
    """
    Computes highest Correlation Coefficient of two xarrays with same spatial
    shape and same timesteps. Returns 3 xarrays in same spatial shape and additional
    dimension "tau" containing 1. Correlation, 2.covariance and 3.
    Correlation Coeff for each tau and spatial shift

    x: First xarray, has to be the one with limited time steps
    y: Second xarray has to have at least tau.max() additional time steps
    tau: np.array with all timeshifts to be computed
    """

    coords = {'tau':tau,'lat_shift':lat_shift,'lon_shift':lon_shift,
        'lat':x.lat.values,'lon':x.lon.values}
    dims = ['tau','lat_shift','lon_shift','lat','lon']
    N = x.time.size
    rho_array = xr.DataArray(coords=coords,dims=dims)
    R_array = xr.DataArray(coords=coords,dims=dims)
    cov_array = xr.DataArray(coords=coords,dims=dims)

    for i in lat_shift:
        for j in lon_shift:
            for t in tau:
                start = pd.to_datetime(x.time[0].values)+pd.DateOffset(days=int(t))
                stop = pd.to_datetime(x.time[-1].values)+pd.DateOffset(days=int(t))
                y_shift = y.sel(time=slice(start,stop))
                temp = np.zeros(x.shape)
                if (i>=0 and j >=0):
                    temp[:,i:,j:] = y_shift.values[:,:x.lat.size-i,:x.lon.size-j]
                elif (i<0) and (j<0):
                    temp[:,:x.lat.size+i,:x.lon.size+j] = y_shift.values[:,-i:,-j:]
                elif (i>=0) and (j<0):
                    temp[:,i:,:x.lon.size+j]=y_shift.values[:,:x.lat.size-i,-j:]
                elif (i<0) and (j>=0):
                    temp[:,:x.lat.size+i,j:]=y_shift.values[:,-i:,:x.lon.size-j]
                else:
                    print('HÄÄÄÄÄÄÄÄÄÄ')
                y_shift.values = temp
                R = 1/N *np.sum(x.values * y_shift.values,axis=0)
                R_array[t,i-lat_shift.min(),j-lon_shift.min()] = R
                cov = (R-x.values.mean(axis=0)*y_shift.values.mean(axis=0))
                cov_array[t,i-lat_shift.min(),j-lon_shift.min()] = cov
                rho = ( cov /
                    (x.values.std(axis=0)*y_shift.values.std(axis=0)) )
                rho_array[t,i-lat_shift.min(),j-lon_shift.min()] = rho

    return R_array,cov_array,rho_array

#%% PREPROCESS:
path = 'D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana.nc'
path_cli = path[:-3]+'_climate.nc'

iron_raw = xr.open_dataarray('D://thesisdata/wrf_dust/fe_dep_advection_land_source_0_Nm.nc')
iron = iron_raw.sel(time=slice('2009-09-18T00','2009-10-02'))[::8]
chl_raw = xr.open_dataset(path)['CHL']
if minus_climate_mean:
    chl_raw_cli = xr.open_dataset(path_cli)['CHL_mean']

#%% GET CURRENT FIELD FOR SHIFTS:
ds = xr.open_dataset('D://thesisdata/currents/position_shifts_starting_2009-09-22+1day')
pos = ds['positions']
idx_pos = ds['idx_pos']
tau_diff_lat = []
tau_diff_lon = []

for t in pos.tau.values:
    tau_diff_lat.append((idx_pos.sel(pos='lat',tau=t)-idx_pos.sel(pos='lat',tau=0)))
    tau_diff_lon.append((idx_pos.sel(pos='lon',tau=t)-idx_pos.sel(pos='lon',tau=0)))

#%% Change values: LOGARITHM and CLIMATE?
if fe_log10:
    iron.values = np.log10(iron.values)
if chl_log10:
    chl_raw.values = np.log10(chl_raw.values)
if minus_climate_mean:
    chl_raw_cli.values = np.log10(chl_raw_cli.values)
    chl_raw.values = chl_raw.values-chl_raw_cli.values
#%% TO Shape of Fe Depositions
chl = chl_raw.interp(coords={'lat':iron.lat.values,'lon':iron.lon.values})
#%% Derivation / Changes:
if dfdt:
    iron = iron.diff('time')
if dcdt:
    chl = chl.diff('time')
#%%
R,cov, rho = corr_tau(iron,chl,tau,lat_shift=np.arange(-shift,shift+1),lon_shift=np.arange(-shift,shift+1))

#%% CREATE ARRAYS WITH IDEAL SHIFT:
R_s = xr.DataArray(dims=['tau','lat','lon'],coords=pos.drop('pos').coords)
cov_s = xr.DataArray(dims=['tau','lat','lon'],coords=pos.drop('pos').coords)
rho_s = xr.DataArray(dims=['tau','lat','lon'],coords=pos.drop('pos').coords)

for t in tau:
    for i in range(124):
        for j in range(164):
            i_s = int(tau_diff_lat[t][i,j])
            j_s = int(tau_diff_lon[t][i,j])
            R_s[t,i,j]=R.sel(lat_shift=i_s,lon_shift=j_s)[t,i,j]
            cov_s[t,i,j]=cov.sel(lat_shift=i_s,lon_shift=j_s)[t,i,j]
            rho_s[t,i,j]=rho.sel(lat_shift=i_s,lon_shift=j_s)[t,i,j]
    print('timestep {:} finished'.format(t))

ds = R.to_dataset(name='R')
ds['cov'] = cov
ds['rho'] = rho
ds['R_s'] = R_s
ds['cov_s'] = cov_s
ds['rho_s'] = rho_s
ds.to_netcdf('D://thesisdata/wrf_dust/correlation_coefficents_230909.nc')
