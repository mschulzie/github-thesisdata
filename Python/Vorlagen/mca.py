import numpy as np
import helperlies as mway
import xarray as xr
import pandas as pd
from warfy import Warfy

# load landmask:
land = Warfy()
land.load_var('LANDMASK')
landmask = land.get_var('LANDMASK').isel(time=0)

tres = 1 #treshold!!
coarse = 20
extent = [145,170,-10,-45]

fe = mway.import_iron_dep().sel(time=slice('2009-09-18T03','2009-09-30T00'))
fe = fe.where(landmask==0)
fe = fe.where(fe.sum('time')>1/(3*60*60))
fe = fe.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[3],extent[2]))
fe.values = fe.values * 3 * 60 * 60
fe = fe.coarsen(time=8,boundary='exact').sum(keep_attrs=True)
fe['time'] = pd.date_range('2009-09-19T00','2009-09-30T00',freq='24h')
fe.attrs['units'] = 'ug/m2/d'
#ADD timeseries with zero deposition:
time_plus = pd.date_range('2009-10-01','2009-10-05',freq='d')
fe_plus = xr.DataArray(np.zeros((time_plus.size,fe.shape[1],fe.shape[2])),
    coords = {'time'  : time_plus,
    'lat'   : fe.lat.values,'lon'   : fe.lon.values},
    dims=['time','lat','lon'])
fe = xr.concat([fe,fe_plus],dim='time')
fe = fe.where(fe.sum('time')>0)
fe.values[fe.values>0] = np.log10(fe.values[fe.values>0])
#%%
path = 'D://thesisdata/plankton/marine_copernicus/2009/'
chl_sep = xr.open_mfdataset(path+'200909*.nc')
chl_okt = xr.open_mfdataset(path+'200910*.nc')
chl = xr.concat([chl_sep,chl_okt],dim='time')
chl = chl.assign_coords(lon=(chl.lon % 360)).roll(lon=(chl.dims['lon'] // 2), roll_coords=True)
chl = chl.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
del(chl_sep,chl_okt)
chl = chl.sel(time=slice('2009-09-23T00','2009-10-09T00'))
chl = chl['CHL']
chl.values = np.log10(chl.values)
chl = chl.coarsen(lon=coarse,lat=coarse,boundary='trim').mean(keep_attrs=True)
#%%
path_cli = 'D://thesisdata/plankton/marine_copernicus/climatology/'
chl_sep = xr.open_mfdataset(path_cli+'199809*.nc')
chl_okt = xr.open_mfdataset(path_cli+'199810*.nc')
chl_cli = xr.concat([chl_sep,chl_okt],dim='time')
chl_cli = chl_cli.assign_coords(lon=(chl_cli.lon % 360)).roll(lon=(chl_cli.dims['lon'] // 2), roll_coords=True)
chl_cli = chl_cli.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
del(chl_sep,chl_okt)
chl_cli = chl_cli.sel(time=slice('1998-09-23T00','1998-10-09T00'))
chl_cli = chl_cli['CHL_mean']
chl_cli.values = np.log10(chl_cli.values)
chl_cli = chl_cli.coarsen(lon=coarse,lat=coarse,boundary='trim').mean(keep_attrs=True)

#%%
# REMOVE MEAN --> zero-mean !! Hier ggf. stattdessen mit KLima-Mittel!!
chl_a = chl.values-chl_cli.values
n_chl = np.product(chl.shape[1:])
n_fe = np.product(fe.shape[1:])
if fe.shape[0]!=chl_a.shape[0]:
    raise KeyError('Different number of time steps!!')
else:
    n_time = fe.shape[0]

# normalize:
#array = array / array.std(dim='time')

# RESHAPE:
chl_a = chl_a.reshape(n_time,n_chl)
fe_a = fe.values.reshape(n_time,n_fe)
#kill NaN:
chl_index = np.where(~(np.isnan(chl_a[0])))[0]
fe_index = np.where(~(np.isnan(fe_a[0])))[0]
fe_a = fe_a[:,fe_index]
chl_a = chl_a[:,chl_index]
chl_a[:,722]=0
# Matrix multiplication
cov = 1/n_time * (fe_a.T @ chl_a)

# SINGULAR VALUE DECOMPOSITION
VLeft, singular_values, VTRight = np.linalg.svd(cov, full_matrices=False)
#%%
#save singular vectors
VLeft = VLeft
VRight = VTRight.T

# Singular Vectors to projections:
S = np.sqrt(np.diag(singular_values)*n_time)
Si = np.diag(1. / np.diag(S))

##loaded singular vectors:
VLeft_L = VLeft @ S
VRight_L = VRight @ S
##
VLeft_U = fe_a @ VLeft @ Si   # == PC's !!!
VRight_U = chl_a @ VRight @ Si  # == PC's!!!

# Create EOF's :
eof_left = np.zeros((n_fe,singular_values.size))
eof_right = np.zeros((n_chl,singular_values.size))

eof_left[fe_index,:] = VLeft
eof_right[chl_index,:] = VRight

# first bring back to array including NaN!!
eof_left = eof_left.reshape(fe.shape[1:]+(singular_values.size,))
eof_right = eof_right.reshape(chl.shape[1:]+(singular_values.size,))
plt.contourf(eof_left[:,:,0])
plt.contourf(eof_right[:,:,0])
x = np.arange()

#%%
# from xmca.xarray import xMCA
# mca = xMCA(fe,chl)
# mca.set_field_names('Fe Dep','CHL_a')
# #mca.normalize()
# mca.solve()
#
# eigenvalues=mca.singular_values()
# mcs = mca.pcs()
# eofs = mca.eofs()
#
# mca.plot(mode=1,orientation='vertical',threshold=0.3)
