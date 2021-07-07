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
from Python.modeloutput.deposition_iron import sections
#%% SETTINGS:
tau = np.arange(11)
dcdt = True
fe_log10 = False
chl_log10 = False
minus_climate_mean = True
norm = SymLogNorm(1e-8,vmin=cov_min,vmax=cov_max,base=10) #None
cmap = 'RdBu_r'
add = ''
#%% Function needed:
def corr_tau(x,y,tau):
    """
    Computes highest Correlation Coefficient of two xarrays with same spatial
    shape and same timedelta. Returns 2 xarrays in same spatial shape and additional
    dimension "tau" containing 1. Correlation and 2. Correlation Coeff for each tau

    x: First xarray, has to be the one with limited time steps
    y: Second xarray has to have at least tau.max() additional time steps
    tau: np.array with all timeshifts to be computed
    """
    N = x.time.size
    rho_array = xr.DataArray(coords={'tau': tau,'lat':x.lat.values,
        'lon':x.lon.values,},dims=['tau','lat','lon'])
    R_array = xr.DataArray(coords={'tau': tau,'lat':x.lat.values,
        'lon':x.lon.values,},dims=['tau','lat','lon'])
    cov_array = xr.DataArray(coords={'tau': tau,'lat':x.lat.values,
        'lon':x.lon.values,},dims=['tau','lat','lon'])

    for t in tau:
        start = pd.to_datetime(x.time[0].values)+pd.DateOffset(days=int(t))
        stop = pd.to_datetime(x.time[-1].values)+pd.DateOffset(days=int(t))
        y_shift = y.sel(time=slice(start,stop))
        R = 1/N *np.sum(x.values * y_shift.values,axis=0)
        R_array[t] = R
        cov = (R-x.values.mean(axis=0)*y_shift.values.mean(axis=0))
        cov_array[t] = cov
        rho = ( cov /
            (x.values.std(axis=0)*y_shift.values.std(axis=0)) )
        rho_array[t] = rho
    return R_array,cov_array,rho_array
#%% PREPROCESS:
path = 'D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana.nc'
path_cli = path[:-3]+'_climate.nc'

iron = mway.import_iron_dep(landmask=True)[1:,...] # drop first timestep
iron = iron.coarsen(time=8,boundary='exact').mean(keep_attrs=True)
iron = iron.assign_coords(time=pd.date_range('2009-09-18','2009-09-29',freq='d'))
chl_raw = xr.open_dataset(path)['CHL']
if minus_climate_mean:
    chl_raw_cli = xr.open_dataset(path_cli)['CHL_mean']
#%% Change values: LOGARITHM and CLIMATE?
if fe_log10:
    iron.values = np.log10(iron.values)
    add+='_fe_log10'
if chl_log10:
    chl_raw.values = np.log10(chl_raw.values)
    add+='_chl_log10'
if minus_climate_mean:
    chl_raw_cli.values = np.log10(chl_raw_cli.values)
    chl_raw.values = chl_raw.values-chl_raw_cli.values
    add+='_climate_corr'
#%% TO Shape of Fe Depositions
chl = chl_raw.interp(coords={'lat':iron.lat.values,'lon':iron.lon.values})

#%% Ableitung / / kill negative values in chl-a?
if dcdt:
    chl = chl.diff('time')
    add+='_dcdt'
#chl.values[chl.values<0]=0 # SET NEGATIVE CHANGES TO ZERO!
#%%
R,cov, rho = corr_tau(iron,chl,tau)
R_idx = R.fillna(0).argmax('tau')
rho_idx = rho.fillna(0).argmax('tau')
cov_idx = cov.fillna(0).argmax('tau')
levels = np.append(tau,tau.max()+1)
R_min, R_max = R.min().values, R.max().values
cov_min, cov_max =  cov.min().values, cov.max().values
#%% PLOTTING

def format_ax(ax,text=None):
    ax.coastlines(lw=.5, zorder=5)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=4)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
    ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
    ax.set_title('')
    if text == None:
        pass
    elif type(text) == str:
        ax.text(-.3, 0.5, text, transform=ax.transAxes,
                size=10)#, weight='bold')
    else:
        ax.text(-.3, 0.5, r'$\tau =$'+str(text), transform=ax.transAxes,
                size=10)#, weight='bold')

fig = plt.figure(figsize=(9,26))
gs = fig.add_gridspec(len(tau)+2,3,wspace=.7)
# PLOT INDEXES:
ax1 = fig.add_subplot(gs[0,0],projection=crs.Mercator(central_longitude=150.0))
ax2 = fig.add_subplot(gs[0,1],projection=crs.Mercator(central_longitude=150.0))
ax3 = fig.add_subplot(gs[0,2],projection=crs.Mercator(central_longitude=150.0))
R_idx.plot(ax=ax1,cmap='viridis',levels=levels,extend='neither',
    transform=crs.PlateCarree())
cov_idx.plot(ax=ax2,cmap='viridis',levels=levels,extend='neither',
    transform=crs.PlateCarree())
rho_idx.plot(ax=ax3,cmap='viridis',levels=levels,extend='neither',
    transform=crs.PlateCarree())
format_ax(ax1,'max\nR'), format_ax(ax2,'max\ncov'), format_ax(ax3,'max\n'+r'$\rho$')
ax1.set_title(r'$\tau$'), ax2.set_title(r'$\tau$'), ax3.set_title(r'$\tau$')
# PLOT MAX CORRELATION
ax1 = fig.add_subplot(gs[1,0],projection=crs.Mercator(central_longitude=150.0))
im1 = R[R_idx].plot(ax=ax1,extend='neither',transform=crs.PlateCarree(),
    cmap=cmap,add_colorbar=False,norm=norm)
    #,)vmin=R_min,vmax=R_max
cb1  = fig.colorbar(im1,shrink=.8)
#cb1.set_ticks([-1e-2,-1e-5,0,1e-5,1e-2])
ax2 = fig.add_subplot(gs[1,1],projection=crs.Mercator(central_longitude=150.0))
im2 = cov[cov_idx].plot(ax=ax2,extend='neither',norm=norm,
    transform=crs.PlateCarree(),cmap=cmap,add_colorbar=False)
cb2  = fig.colorbar(im2,shrink=.8)
ax3 = fig.add_subplot(gs[1,2],projection=crs.Mercator(central_longitude=150.0))
im3 = rho[rho_idx].plot(ax=ax3,extend='neither',vmin=-1,vmax=1,
    transform=crs.PlateCarree(),cmap=cmap,add_colorbar=False)
cb3  = fig.colorbar(im3,shrink=.8)
cb3.set_ticks([-1,-0.5,0,0.5,1])
format_ax(ax1,'max\nR'), format_ax(ax2,'max\ncov'), format_ax(ax3,'max\n'+r'$\rho$')
ax1.set_title(r'$R(\tau)$'), ax2.set_title(r'$cov(\tau)$'), ax3.set_title(r'$\rho(\tau)$')
#PLOT EACH TAU
for i,t in enumerate(tau):
    ax1 = fig.add_subplot(gs[i+2,0],projection=crs.Mercator(central_longitude=150.0))
    ax2 = fig.add_subplot(gs[i+2,1],projection=crs.Mercator(central_longitude=150.0))
    ax3 = fig.add_subplot(gs[i+2,2],projection=crs.Mercator(central_longitude=150.0))

    R.sel(tau=t).plot(ax=ax1,extend='neither',transform=crs.PlateCarree(),
        cmap=cmap,add_colorbar=False,norm=norm)
        #,vmin=R_min,vmax=R_max
    cov.sel(tau=t).plot(ax=ax2,extend='neither',
        transform=crs.PlateCarree(),cmap=cmap,norm=norm,
        add_colorbar=False)
    rho.sel(tau=t).plot(ax=ax3,extend='neither',vmin=-1,vmax=1,
        transform=crs.PlateCarree(),cmap=cmap,
        add_colorbar=False)
    format_ax(ax1,t), format_ax(ax2,t), format_ax(ax3,t)

line = plt.Line2D((.33,.33),(.13,.87), color="grey", linewidth=1,linestyle='--')
line2 = plt.Line2D((.66,.66),(.13,.87), color="grey", linewidth=1,linestyle='--')
fig.add_artist(line)
fig.add_artist(line2)

fig.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/correlation'+
        add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
#%% SECTIONS MEANS DEPENDENCY FROM TAU
fig2 = plt.figure(figsize=(10,4))
gs2 = fig2.add_gridspec(3,2,hspace=.2,wspace=.2)

for i,ort in enumerate(sections):
    ax = fig2.add_subplot(gs2[i])
    ax.plot(tau,cov.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat')),
        label=ort,color='black')
    ax.set_xticks(tau)
    ax.grid(axis='x')
    ax.legend()
    if i < 4:
        ax.set_xticklabels('')
    else:
        ax.set_xlabel(r'$\tau$')
fig2.suptitle('Mittlere Kovarianzen')
fig2.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/section_correlation'+
        add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
