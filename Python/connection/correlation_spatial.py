import xarray as xr
import helperlies as mway
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from warfy import Warfy

#%% Function needed:
def corr_tau(x,y,tau):
    """
    Computes highest Correlation Coefficient of two xarrays with same spatial
    shape and same timedelta. Returns xarray in same spatial shape and additional
    dimension "tau" containing Correlation Coeff for each tau

    x: First xarray, has to be the one with limited time steps
    y: Second xarray has to have at least tau.max() additional time steps
    tau: np.array with all timeshifts to be computed
    """
    N = x.time.size
    coeff_array = xr.DataArray(coords={'tau': tau,'lat':x.lat.values,
        'lon':x.lon.values,},dims=['tau','lat','lon'])

    for t in tau:
        start = pd.to_datetime(x.time[0].values)+pd.DateOffset(days=int(t))
        stop = pd.to_datetime(x.time[-1].values)+pd.DateOffset(days=int(t))
        y_shift = y.sel(time=slice(start,stop))
        R = 1/N *np.sum(x.values * y_shift.values,axis=0)
        C = ( (R-x.values.mean(axis=0)*y_shift.values.mean(axis=0)) /
            (x.values.std(axis=0)*y_shift.values.std(axis=0)) )
        coeff_array[t] = C
    return coeff_array
#%%
path = 'D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana.nc'

iron = mway.import_iron_dep(landmask=True)[1:,...] # drop first timestep
iron = iron.coarsen(time=8,boundary='exact').mean(keep_attrs=True)
iron = iron.assign_coords(time=pd.date_range('2009-09-18','2009-09-29',freq='d'))
chl_raw = xr.open_dataset(path)['CHL']
chl = chl_raw.interp(coords={'lat':iron.lat.values,'lon':iron.lon.values})
#%% LOGARITHMUS??
#chl.values = np.log10(chl.values)
#iron.values = np.log10(iron.values)
#%% Ableitung
chl = chl.diff('time')
#%%
tau = np.arange(10)
coeff = corr_tau(iron,chl,tau)
highidx = coeff.fillna(0).argmax('tau')
levels = np.append(tau,tau.max()+1)
#highidx.plot(cmap='viridis',levels=levels,extend='neither')
coeff.sel(tau=6).plot()
