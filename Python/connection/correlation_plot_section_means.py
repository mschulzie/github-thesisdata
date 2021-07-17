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
from matplotlib.ticker import FormatStrFormatter
from scipy.stats import pearsonr

path = 'D://thesisdata/plankton/marine_copernicus/2009_prep_corr_ana.nc'
path_cli = path[:-3]+'_climate.nc'
masks = xr.open_dataset('D://thesisdata/wrf_dust/land_and_coast_mask.nc')
land = masks['land']
coast = masks['coast']
iron_raw = mway.import_iron_dep()[1:]
iron_tres = (iron_raw.sum('time')*60*60*3)
iron = iron_raw.coarsen(time=8).mean(keep_attrs=True)
iron = iron.assign_coords(time=pd.date_range('2009-09-18T00','2009-09-29T00',freq='d'))
chl_raw = xr.open_dataset(path)['CHL']
chl_raw_cli = xr.open_dataset(path_cli)['CHL_mean']
chl_raw_cli = chl_raw_cli.assign_coords(time=chl_raw.time)
chl = (chl_raw-chl_raw_cli).diff('time')
chl = chl.interp(coords=iron.drop('time').coords)
chl = chl.where(land==0)
chl = chl.where(coast==0)
#chl = chl.where(iron_tres>5)

mean_chla = {}
mean_iron = {}
R = {}
cov = {}
rho = {}
p = {}
tau = np.arange(11)
N = iron.time.size

for ort in sections:
    mean_chla[ort]= chl.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat'))
    mean_iron[ort]= iron.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat'))

for ort in sections:
    R[ort] = np.zeros(len(tau))
    cov[ort] = np.zeros(len(tau))
    rho[ort] = np.zeros(len(tau))
    p[ort] = [None]*(len(tau))
    for t in tau:
        start = pd.to_datetime(iron.time[0].values)+pd.DateOffset(days=int(t))
        stop = pd.to_datetime(iron.time[-1].values)+pd.DateOffset(days=int(t))
        y_shift = mean_chla[ort].sel(time=slice(start,stop))
        p[ort][t] = pearsonr(mean_iron[ort].values,y_shift.values)
        R[ort][t] = 1/N *np.sum(mean_iron[ort].values * y_shift.values,axis=0)
        cov[ort][t] = (R[ort][t]-mean_iron[ort].values.mean(axis=0)*y_shift.values.mean(axis=0))
        rho[ort][t] = ( cov[ort][t] /
            (mean_iron[ort].values.std(axis=0)*y_shift.values.std(axis=0)) )

fig2 = plt.figure(figsize=(10,4))
gs2 = fig2.add_gridspec(3,2,hspace=.2,wspace=0.5)
ax_color = '#3b3f61'
ax2_color = '#c45454'
for i,ort in enumerate(sections):
    print(rho[ort].max())
    ax = fig2.add_subplot(gs2[i])
    ax2 = ax.twinx()
    #ax2.set_ylim(0,1.1)
    ax2.set_ylabel(r'$ \rho_\mu (\tau)$')
    ax.set_ylabel(r' cov$_\mu(\tau)$')
    ax.plot(tau,cov[ort],color=ax_color)
    ax2.plot(tau,rho[ort],color=ax2_color)
    ax2.text(0.01,0.07,ort,transform=ax.transAxes,
        bbox={'facecolor': 'white', 'pad': 1},zorder=3)
    ax.text(0.01,0.07,ort,transform=ax.transAxes,
        bbox={'facecolor': 'white', 'pad': 1},zorder=3)
    ax.set_xticks(tau)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0e'))
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.tick_params(axis='y',labelsize=8)
    ax2.yaxis.label.set_color(ax2_color)
    ax.yaxis.label.set_color(ax_color)
    ax2.tick_params(axis='y',colors=ax2_color)
    ax.tick_params(axis='y',colors=ax_color)
    ax.grid(axis='x')
    if i < 4:
        ax.set_xticklabels('')
    else:
        ax.set_xlabel(r'$\tau$')

line = plt.Line2D((.51,.51),(.07,.87), color="grey", linewidth=1,linestyle='--')
fig2.add_artist(line)
#fig2.suptitle('Kreuz-Korrelation/-Kovarianz gemittelt')
fig2.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/section_means_crosscorr_noadv'
        +'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
