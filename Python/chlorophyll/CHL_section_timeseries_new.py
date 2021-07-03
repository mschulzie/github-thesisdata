import xarray as xr
import helperlies as mway
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as mdates
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)
from matplotlib.colors import LogNorm
import os
import string

tres = 5
#ort = 'Tasman'
from Python.modeloutput.deposition_iron import sections
which= ['Nordost','Korall','Tasman','Süden','Südozean']
sections = {key: sections[key] for key in which}
cl_mean_0 = {}
cl_max_0 = {}
cl_min_0 = {}
cl_std_0 = {}
cl_mean = {}
cl_max = {}
cl_min = {}
cl_std = {}
chl_0 = {}
chl_err_0 = {}
chl = {}
chl_err = {}
for ort in sections:
        cl_mean_0[ort] = []
        cl_max_0[ort] = []
        cl_min_0[ort] = []
        cl_std_0[ort] = []
        cl_mean[ort] = []
        cl_max[ort] = []
        cl_min[ort] = []
        cl_std[ort] = []
        chl[ort] = []
        chl_err[ort] = []
        chl_0[ort] = []
        chl_err_0[ort] = []

path = 'D://thesisdata/plankton/marine_copernicus/climatology/'
dir = os.listdir(path)
#% #Create mask via interpolation of deposition data:
ds = xr.open_dataset(path+dir[0]).drop('time')
ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
ds = ds.sel(lat=slice(-9.89,-57.06),lon=slice(110.3,189.7))
from Python.modeloutput.deposition_iron import total_sum
total_sum = total_sum.interp(coords=ds.coords)
#%
for file in dir:
    ds = xr.open_dataset(path+file)
    for ort in sections:
        total_sum_dt = total_sum.sel(lon=slice(sections[ort][0],sections[ort][1]),
            lat=slice(sections[ort][2],sections[ort][3]))
        dt = ds.sel(lon=slice(sections[ort][0],sections[ort][1]),
            lat=slice(sections[ort][2],sections[ort][3]))
        cl_mean_0[ort].append(dt['CHL_mean'].mean(dim=('lon','lat')).values[0])
        cl_max_0[ort].append(dt['CHL_percentile_97'].mean(dim=('lon','lat')).values[0])
        cl_min_0[ort].append(dt['CHL_percentile_3'].mean(dim=('lon','lat')).values[0])
        cl_std_0[ort].append(dt['CHL_standard_deviation'].mean(dim=('lon','lat')).values[0])
        dt = dt.where(total_sum_dt>tres)
        cl_mean[ort].append(dt['CHL_mean'].mean(dim=('lon','lat')).values[0])
        cl_max[ort].append(dt['CHL_percentile_97'].mean(dim=('lon','lat')).values[0])
        cl_min[ort].append(dt['CHL_percentile_3'].mean(dim=('lon','lat')).values[0])
        cl_std[ort].append(dt['CHL_standard_deviation'].mean(dim=('lon','lat')).values[0])


#% # Nun für 2009:
path = 'D://thesisdata/plankton/marine_copernicus/2009/'

for file in os.listdir(path):
    ds = xr.open_dataset(path+file)
    for ort in sections:
        total_sum_dt = total_sum.sel(lon=slice(sections[ort][0],sections[ort][1]),
            lat=slice(sections[ort][2],sections[ort][3]))
        dt = ds.sel(lon=slice(sections[ort][0],sections[ort][1]),
            lat=slice(sections[ort][2],sections[ort][3]))
        chl_0[ort].append(dt['CHL'].mean(dim=('lon','lat')).values[0])
        chl_err_0[ort].append(dt['CHL_error'].mean(dim=('lon','lat')).values[0])
        dt = dt.where(total_sum_dt>tres)
        chl[ort].append(dt['CHL'].mean(dim=('lon','lat')).values[0])
        chl_err[ort].append(dt['CHL_error'].mean(dim=('lon','lat')).values[0])

#%%
for ort in sections:
    cl_mean[ort] = np.array(cl_mean[ort])
    cl_max[ort] = np.array(cl_max[ort])
    cl_min[ort] = np.array(cl_min[ort])
    cl_std[ort] = np.array(cl_std[ort])
    cl_mean_0[ort] = np.array(cl_mean_0[ort])
    cl_max_0[ort] = np.array(cl_max_0[ort])
    cl_min_0[ort] = np.array(cl_min_0[ort])
    cl_std_0[ort] = np.array(cl_std_0[ort])
    chl[ort] = np.array(chl[ort])
    chl_err[ort] = np.array(chl_err[ort])
    chl_err[ort] = chl[ort] * chl_err[ort]/100
    chl_0[ort] = np.array(chl_0[ort])
    chl_err_0[ort] = np.array(chl_err_0[ort])
    chl_err_0[ort] = chl_0[ort] * chl_err_0[ort]/100

#%%
# Now PLOTTING:
def format_ax(ax,ylim=True):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
    ax.tick_params(axis='x', labelrotation=0)
    ax.legend(fontsize=6)
    ax.grid(axis='x')
    ax.set_xlim('2009-06-01','2009-12-31')
    ax.set_xticklabels('')
    if ylim:
        ax.set_ylim(0,1)
        ax.set_yticks(np.arange(0.2,1.2,0.2))

t = pd.date_range('2009-06-01','2009-12-31',freq='d')
rows, cols = len(sections),2
fig = plt.figure(figsize=(10,rows*2.5))
gs = fig.add_gridspec(rows,cols,hspace=0.1)
ax1,ax2 = {},{}
for i,ort in enumerate(sections):
    ax1[ort]= (fig.add_subplot(gs[i,0]))
    ax2[ort]= (fig.add_subplot(gs[i,1]))
    ax1[ort].plot(t,chl_0[ort],color='#ff2e00',label=r'$\mu_C(t)$')
    ax1[ort].plot(t,cl_mean_0[ort],label=r'$\mu_{C,cli}(t)$',color='#0037a1')
    ax1[ort].fill_between(t,cl_min_0[ort],cl_max_0[ort],label=r'$\mu_{q_{0.03}}(t)$, $\mu_{q_{0.97}}(t)$',
        color='#13e3be',facecolor='#c1fbf6')
    ax1[ort].fill_between(t,chl_0[ort]-chl_err_0[ort],chl_0[ort]+chl_err_0[ort],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    ax1[ort].fill_between(t,cl_mean_0[ort]-cl_std_0[ort],cl_mean_0[ort]+cl_std_0[ort],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    format_ax(ax1[ort])
    ax1[ort].text(pd.to_datetime('2009-06-03'),0.98,
        '{:}° bis {:}° E und {:}° bis {:}° S\n({:})'.format(
        sections[ort][0],sections[ort][1],sections[ort][2]*-1,sections[ort][3]*-1,ort),
        va='top',bbox={'facecolor': 'white', 'alpha': .8, 'pad': 1})
    #RECHTE SEITE:
    ax2[ort].plot(t,chl[ort]-cl_mean[ort],color='#ff2e00' ,
        label=r'$\Delta \mu_C (t)$')
    ax2[ort].fill_between(t,chl[ort]-cl_mean[ort]-chl_err[ort],chl[ort]-cl_mean[ort]+chl_err[ort],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    ax2[ort].plot(t,np.zeros(t.size),color='black')
    ax2[ort].fill_between(t,-cl_std[ort],cl_std[ort],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    format_ax(ax2[ort],ylim=False)
    ax1[ort].text(1.02, 0.5, string.ascii_uppercase[i], transform=ax1[ort].transAxes,
            size=20, weight='bold')
ax1[list(sections)[0]].set_title('Rohdaten uneingeschränkt')
ax2[list(sections)[0]].set_title(r'Trend bereinigt und $m_{Fe}/A>$'+'{:.1f} ug/m2'.format(
    tres))
ax1[list(sections)[len(sections)//2]].set_ylabel('CHL-a Konzentrationen in mg/m3',fontsize=12)
ax1[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax1[list(sections)[-1]].tick_params(axis='x', labelrotation=0)
ax2[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax2[list(sections)[-1]].tick_params(axis='x', labelrotation=0)

plt.tight_layout()
fig.savefig('./Thesis/bilder/timeseries_all.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
plt.show()
