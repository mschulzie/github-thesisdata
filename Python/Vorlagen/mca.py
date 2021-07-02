import numpy as np
import helperlies as mway
import xarray as xr
import pandas as pd
from warfy import Warfy
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

#SETTINGS:
tres = 1 #treshold!!
coarse = 10
extent = [110,179,-10,-57]
time_shift = 5
iron_period = [pd.to_datetime('2009-09-19'),pd.to_datetime('2009-10-05')]
chl_period = [iron_period[0]+pd.DateOffset(days=time_shift),
    iron_period[1]+pd.DateOffset(days=time_shift)]
mask_chl = False # mask with fe treshold
mask_fe = True # mask with fe treshold

mode = 1
# load landmask:
land = Warfy()
land.load_var('LANDMASK')
landmask = land.get_var('LANDMASK').isel(time=0)

fe = mway.import_iron_dep().sel(time=slice('2009-09-18T03','2009-09-30T00'))
fe_raw_sum = fe.sum('time') * 3*60*60
fe = fe.where(landmask==0)
if mask_fe:
    fe_mask = fe.sum('time')>tres/(3*60*60)
    fe = fe.where(fe_mask)
fe = fe.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[3],extent[2]))
fe.values = fe.values * 3 * 60 * 60
fe = fe.coarsen(time=8,boundary='exact').sum(keep_attrs=True)
fe['time'] = pd.date_range('2009-09-19T00','2009-09-30T00',freq='24h')
fe.attrs['units'] = 'ug/m2/d'
#ADD timeseries with zero deposition:
time_plus = pd.date_range('2009-10-01',iron_period[1],freq='d')
fe_plus = xr.DataArray(np.zeros((time_plus.size,fe.shape[1],fe.shape[2])),
    coords = {'time'  : time_plus,
    'lat'   : fe.lat.values,'lon'   : fe.lon.values},
    dims=['time','lat','lon'])
fe = xr.concat([fe,fe_plus],dim='time')
fe = fe.where(fe.sum('time')>0)
#fe.values[fe.values>0] = np.log10(fe.values[fe.values>0])
#%%
path = 'D://thesisdata/plankton/marine_copernicus/2009/'
chl_sep = xr.open_mfdataset(path+'200909*.nc')
chl_okt = xr.open_mfdataset(path+'200910*.nc')
chl = xr.concat([chl_sep,chl_okt],dim='time')
chl = chl.assign_coords(lon=(chl.lon % 360)).roll(lon=(chl.dims['lon'] // 2), roll_coords=True)
chl = chl.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
del(chl_sep,chl_okt)
chl = chl.sel(time=slice(chl_period[0],chl_period[1]))
chl = chl['CHL']
#chl.values = np.log10(chl.values)
chl = chl.coarsen(lon=coarse,lat=coarse,boundary='trim').mean(keep_attrs=True)
#%%
path_cli = 'D://thesisdata/plankton/marine_copernicus/climatology/'
chl_sep = xr.open_mfdataset(path_cli+'199809*.nc')
chl_okt = xr.open_mfdataset(path_cli+'199810*.nc')
chl_cli = xr.concat([chl_sep,chl_okt],dim='time')
chl_cli = chl_cli.assign_coords(lon=(chl_cli.lon % 360)).roll(lon=(chl_cli.dims['lon'] // 2), roll_coords=True)
chl_cli = chl_cli.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
del(chl_sep,chl_okt)
chl_cli = chl_cli.sel(time=slice('1998'+str(chl_period[0])[4:10],'1998'
    +str(chl_period[1])[4:10]))
chl_cli = chl_cli['CHL_mean']
#chl_cli.values = np.log10(chl_cli.values)
chl_cli = chl_cli.coarsen(lon=coarse,lat=coarse,boundary='trim').mean(keep_attrs=True)
#%%
# REMOVE MEAN --> zero-mean !! Hier stattdessen mit KLima-Mittel!!
chl_a = xr.DataArray(chl.values-chl_cli.values,coords=chl.coords,dims=chl.dims)
# Mask with treshold FE input and LAND
if mask_chl:
    fe_raw_sum = fe_raw_sum.where(landmask==0)
    fe_interp = fe_raw_sum.interp(coords=chl.drop('time').coords)
    chl_a = chl_a.where(fe_interp>tres).values
else:
    chl_a = chl_a.values
#chl_a = chl.values -chl.values.mean(axis=0) # FALLS MEAN = 0 gefordert
#fe.values = fe.values - fe.values.mean(axis=0) # FALLS MEAN = 0 gefordert
n_chl = np.product(chl.shape[1:])
n_fe = np.product(fe.shape[1:])
if fe.shape[0]!=chl_a.shape[0]:
    raise KeyError('Different number of time steps!!')
else:
    n_time = fe.shape[0]

# normalize:
fe_a = fe.values / fe.values.std(axis=0)
chl_a = chl_a /chl_a.std(axis=0)

# RESHAPE:
chl_a = chl_a.reshape(n_time,n_chl)
fe_a = fe_a.reshape(n_time,n_fe)
#kill NaN:
chl_index = np.where(~(np.isnan(chl_a[0])))[0]
fe_index = np.where(~(np.isnan(fe_a[0])))[0]
fe_a = fe_a[:,fe_index]
chl_a = chl_a[:,chl_index]
#chl_a[:,722]=0
# Matrix multiplication
cov = 1/n_time * (fe_a.T @ chl_a)

# SINGULAR VALUE DECOMPOSITION
VLeft, singular_values, VTRight = np.linalg.svd(cov, full_matrices=False)
VLeft.shape
VTRight.shape
singular_values.shape
fe_a.shape
chl_a.shape
#%%
#save singular vectors
VLeft = VLeft
VRight = VTRight.conjugate().T

# Singular Vectors to projections:
S = np.sqrt(np.diag(singular_values)*n_time)
Si = np.diag(1. / np.diag(S))

##loaded singular vectors:
VLeft_L = VLeft @ S
VRight_L = VRight @ S
##
VLeft_U = fe_a @ VLeft @ Si   # == PC's !!!
VRight_U = chl_a @ VRight @ Si  # == PC's!!!

#Scaling PCS:
VLeft_U /= np.nanmax(abs(VLeft_U.real),axis=0)
VRight_U /= np.nanmax(abs(VRight_U.real),axis=0)

# Create EOF's :
eof_left = np.zeros((n_fe,singular_values.size)) * np.nan
eof_right = np.zeros((n_chl,singular_values.size)) *np.nan
VLeft_U.shape
VRight_U.shape
eof_left[fe_index,:] = VLeft
eof_right[chl_index,:] = VRight

# first bring back to array including NaN!!
eof_left = eof_left.reshape(fe.shape[1:]+(singular_values.size,))
eof_right = eof_right.reshape(chl.shape[1:]+(singular_values.size,))
eof_left.shape
eof_iron = xr.DataArray(eof_left,coords = {'lat'   : fe.lat.values,
    'lon'   : fe.lon.values, 'mode':np.arange(1,singular_values.size+1)}
    ,dims=['lat','lon','mode'])
eof_left.shape
62*51
eof_chl = xr.DataArray(eof_right,coords = {'lat'   : chl.lat.values,
    'lon'   : chl.lon.values, 'mode':np.arange(1,singular_values.size+1)}
    ,dims=['lat','lon','mode'])
#SCALING EOF:
eof_iron /= np.nanmax(abs(eof_iron.real),axis=(0,1))
eof_chl /= np.nanmax(abs(eof_chl.real),axis=(0,1))

#%%
fig = plt.figure(figsize=(8,5))
fig.suptitle('Mode = {:}, beschreibt {:.1f}%'.format(
    mode,100*singular_values[mode-1] / singular_values.sum()))
gs = fig.add_gridspec(2,2,height_ratios=[2,1])
ax1 = fig.add_subplot(gs[0],projection=crs.Mercator(central_longitude=150.0))
ax2 = fig.add_subplot(gs[1],projection=crs.Mercator(central_longitude=150.0))
eof_iron.sel(mode=mode).plot(ax=ax1,transform=crs.PlateCarree(),vmin=-1,vmax=1,
    cmap='RdBu_r')
eof_chl.sel(mode=mode).plot(ax=ax2,transform=crs.PlateCarree(),
    cmap='RdBu_r')
ax1.coastlines(lw=.5, zorder=5)
ax1.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax1.add_feature(cfeature.LAND, fc='lightgrey', zorder=3,alpha=.7)
ax1.add_feature(cfeature.STATES,lw=.2, zorder=0)
ax1.set_title('Eisen')
ax2.coastlines(lw=.5, zorder=5)
ax2.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax2.add_feature(cfeature.LAND, fc='lightgrey', zorder=3,alpha=.7)
ax2.add_feature(cfeature.STATES,lw=.2, zorder=0)
ax2.set_title('Chlorophyll-a')
ax1.set_extent(extent,crs=crs.PlateCarree())
ax2.set_extent(extent,crs=crs.PlateCarree())


ax3 = fig.add_subplot(gs[2])
ax3.plot(pd.date_range(iron_period[0],iron_period[1],freq='d'),VLeft_U[:,mode-1])
ax4 = fig.add_subplot(gs[3])
ax4.plot(pd.date_range(chl_period[0],chl_period[1],freq='d'),VRight_U[:,mode-1])
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
ax3.xaxis.set
ax3.tick_params(axis='x', labelrotation=45,size=5)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
ax4.tick_params(axis='x', labelrotation=45,size=5)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax3.set_ylim(-1.2, 1.2)
ax4.set_ylim(-1.2, 1.2)

fig.savefig('D://thesisdata/bilder/Python/wrf_chla/'+str(extent)+'shiftdays_'+str(mode)
    +str(time_shift)+'.png',dpi=300)
#%% Rieger's
# from xmca.array import MCA
# mca = MCA(fe_a,chl_a)
# mca.set_field_names('Fe Dep','CHL_a')
# #mca.normalize()
# mca.solve()
# #eigenvalues=mca.singular_values()
# #mcs = mca.pcs()
# #eofs = mca.eofs()
# mca.plot(mode=1)
