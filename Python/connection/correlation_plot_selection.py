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

ds = xr.open_dataset('D://thesisdata/wrf_dust/correlation_coefficents_230909without_advection.nc')
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
    ax.add_feature(cfeature.STATES,lw=.2, zorder=5)
    ax.set_extent([110,189,-10,-57],crs=crs.PlateCarree())
    ax.set_title('')
    if text == None:
        pass
    elif type(text) == str:
        ax.text(0.05, 0.05, text, transform=ax.transAxes,
                size=10,bbox={'facecolor': 'white', 'pad': 1})#, weight='bold')
    else:
        ax.text(0.05, 0.05, r'$\tau =$'+str(text), transform=ax.transAxes,
                size=10,bbox={'facecolor': 'white', 'pad': 1})#, weight='bold')
#%% PLOTTING
fig = plt.figure(figsize=(10,11))
gs = fig.add_gridspec(4,3,wspace=0.05,hspace=0.05,width_ratios=[1,1,1],
    height_ratios=[2.5,2.5,2.5,3])
# PLOT INDEXES:
ax00 = fig.add_subplot(gs[0,0],projection=crs.Mercator(central_longitude=150.0))
im00= rho_idx.plot(ax=ax00,cmap='jet',levels=levels,extend='neither',
    transform=crs.PlateCarree(),add_colorbar=False)
format_ax(ax00)
ax00.set_title(r'$\tau_\max$')
ax00.text(0,1.03,string.ascii_uppercase[0],transform=ax00.transAxes,
    size=20,weight='bold')
gs20 = gs[1,0].subgridspec(2,3,height_ratios=[1,10],width_ratios=[1,8,1])
cax_20 = fig.add_subplot(gs20[0,1])
cb00 = fig.colorbar(im00,cax=cax_20,orientation='horizontal',shrink=0.8,pad=0.01)#,anchor=(0.2,0.2))
# PLOT MAX CORRELATIONCOEFF:
ax10 = fig.add_subplot(gs[2,0],projection=crs.Mercator(central_longitude=150.0))
im10= rho[rho_idx].plot(ax=ax10,extend='neither',transform=crs.PlateCarree(),
    cmap=cmap,vmin=-1,vmax=1,add_colorbar=False,levels=11)
format_ax(ax10)
ax10.set_title(r'$\rho(\tau_\max)$')
ax10.text(0,1.03,string.ascii_uppercase[1],transform=ax10.transAxes,
    size=20,weight='bold')
gs30 = gs[3,0].subgridspec(2,3,height_ratios=[1,10],width_ratios=[1,8,1])
cax_30 = fig.add_subplot(gs30[0,1])
cb10 = fig.colorbar(im10,cax=cax_30,orientation='horizontal',shrink=0.8,pad=0.01)#,anchor=(0.8,0.8))
cb10.set_ticks([-1,0.5,0,-0.5,1])

#PLOT SELECTION of tau:
tau_sel = [0,1,4,8]

for i,t in enumerate(tau_sel):
    ax_1 = fig.add_subplot(gs[i,1],projection=crs.Mercator(central_longitude=150.0))

    im_1 = rho.sel(tau=t).plot(ax=ax_1,extend='neither',vmin=-1,vmax=1,
        transform=crs.PlateCarree(),cmap=cmap,
        add_colorbar=False,levels=11)
    if i == len(tau_sel)-1:
        cb_1=fig.colorbar(im_1,shrink=.8,orientation='horizontal',pad=0.01)
        cb_1.set_ticks([-1,0.5,0,-0.5,1])
    ax_2 = fig.add_subplot(gs[i,2],projection=crs.Mercator(central_longitude=150.0))
    im_2 = cov.sel(tau=t).plot(ax=ax_2,extend='neither',
        transform=crs.PlateCarree(),cmap=cmap,norm=norm,levels=11,
        add_colorbar=False)
    format_ax(ax_1,t), format_ax(ax_2,t)
    if i == len(tau_sel)-1:
        cb_2=fig.colorbar(im_2,shrink=.8,orientation='horizontal',pad=0.01)
        cb_2.set_ticks([-1e-8,-1e-3,0,1e-2,1e-3,1e-8])
    if i==0:
        ax_1.set_title(r'$\rho(\tau)$')
        ax_2.set_title(r'cov$(\tau)$')
        ax_1.text(0,1.03,string.ascii_uppercase[2],transform=ax_1.transAxes,
            size=20,weight='bold')
        ax_2.text(0,1.03,string.ascii_uppercase[3],transform=ax_2.transAxes,
            size=20,weight='bold')

line = plt.Line2D((.38,.38),(.13,.89), color="grey", linewidth=1,linestyle='--')
line2 = plt.Line2D((.644,.644),(.13,.89), color="grey", linewidth=1,linestyle='--')
line3 = plt.Line2D((.13,.38),(.55,.55), color="grey", linewidth=1,linestyle='--')
fig.add_artist(line)
fig.add_artist(line2)
fig.add_artist(line3)

fig.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/'
        +'correlation_selection'+add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
#%% SECTIONS MEANS DEPENDENCY FROM TAU
from Python.modeloutput.deposition_iron import sections
from matplotlib.ticker import FormatStrFormatter
sections

fig2 = plt.figure(figsize=(10,4))
gs2 = fig2.add_gridspec(3,2,hspace=.2,wspace=0.5)
ax_color = '#3b3f61'
ax2_color = '#c45454'
for i,ort in enumerate(sections):
    ax = fig2.add_subplot(gs2[i])
    ax2 = ax.twinx()
    #ax2.set_ylim(0,1.1)
    ax2.set_ylabel(r'$\mu [\rho (\tau)]$')
    ax.set_ylabel(r'$\mu$ [cov$(\tau)]$')
    ax.plot(tau,cov.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat')),
        label=r'cov$(\tau)$',color=ax_color)
    ax2.plot(tau,rho.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat')),
        label=r'$\rho(\tau)$',color=ax2_color)
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
fig2.savefig('D://thesisdata/bilder/Python/wrf_chla/correlation/section_crosscorr_noadv'+
        add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
