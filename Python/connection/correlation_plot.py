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

ds = xr.open_dataset('D://thesisdata/wrf_dust/correlation_coefficents_230909.nc')
R = ds['R_s']
cov = ds['cov_s']
rho = ds['rho_s']
#%%
R_idx = R.fillna(0).argmax(dim=('tau'))
rho_idx = rho.fillna(0).argmax(dim=('tau'))
cov_idx = cov.fillna(0).argmax(dim=('tau'))
tau = R.tau.values
#%% SETTINGS
cmap = 'RdBu_r'
add = ''
levels = np.append(tau,tau.max()+1)
R_min, R_max = R.min().values, R.max().values
cov_min, cov_max =  cov.min().values, cov.max().values
norm = SymLogNorm(1e-10,vmin=cov_min,vmax=cov_max,base=10) #None
#%% PLOT FORMAT
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
#%% PLOTTING
fig = plt.figure(figsize=(9,26))
gs = fig.add_gridspec(len(tau)+2,3,wspace=.7,hspace=0)
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

fig.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/'
        +'correlation_perfect_spatial_shift_'+add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
#%% SECTIONS MEANS DEPENDENCY FROM TAU
from Python.modeloutput.deposition_iron import sections
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
fig2.suptitle('Kreuz-Kovarianz gemittelt')
fig2.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/section_crosscov'+
        add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)

fig2 = plt.figure(figsize=(10,4))
gs2 = fig2.add_gridspec(3,2,hspace=.2,wspace=.2)

for i,ort in enumerate(sections):
    ax = fig2.add_subplot(gs2[i])
    ax.plot(tau,rho.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat')),
        label=ort,color='black')
    ax.set_xticks(tau)
    ax.grid(axis='x')
    ax.legend()
    if i < 4:
        ax.set_xticklabels('')
    else:
        ax.set_xlabel(r'$\tau$')
fig2.suptitle('Korrelationskoeffizienten gemittelt')
fig2.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/section_corrcoeff'+
        add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
