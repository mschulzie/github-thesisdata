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

tres = 0
ort = 'Tasman'
from Python.modeloutput.deposition import sections

for ort in sections:
    path = 'D://thesisdata/plankton/marine_copernicus/climatology/'
    dir = os.listdir(path)
    section = sections[ort]
    lon = slice(section[0],section[1])
    lat = slice(section[2],section[3])
    #% #Create mask via interpolation of deposition data:
    ds = xr.open_dataset(path+dir[0]).drop('time')
    ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
    ds = ds.sel(lat=slice(-9.89,-57.06),lon=slice(110.3,189.7))
    from Python.modeloutput.deposition import total_sum
    total_sum = total_sum.interp(coords=ds.coords)
    total_sum = total_sum.sel(lon=lon,lat=lat)
    #%
    cl_mean = []
    cl_max = []
    cl_min = []
    cl_std = []
    for file in dir:
        ds = xr.open_dataset(path+file)
        ds = ds.sel(lon=lon,lat=lat)
        ds = ds.where(total_sum>tres)
        cl_mean.append(ds['CHL_mean'].mean(dim=('lon','lat')).values[0])
        cl_max.append(ds['CHL_percentile_97'].mean(dim=('lon','lat')).values[0])
        cl_min.append(ds['CHL_percentile_3'].mean(dim=('lon','lat')).values[0])
        cl_std.append(ds['CHL_percentile_standard_deviation'].mean(dim=('lon','lat')).values[0])
    cl_mean = np.array(cl_mean)
    cl_max = np.array(cl_max)
    cl_min = np.array(cl_min)
    cl_std = np.array(cl_std)
    #% # Nun für 2009:
    path = 'D://thesisdata/plankton/marine_copernicus/2009/'
    chl = []
    chl_err = []
    for file in os.listdir(path):
        ds = xr.open_dataset(path+file)
        ds = ds.sel(lon=lon,lat=lat)
        ds = ds.where(total_sum>tres)
        chl.append(ds['CHL'].mean(dim=('lon','lat')).values[0])
        chl_err.append(ds['CHL_error'].mean(dim=('lon','lat')).values[0])
    chl = np.array(chl)
    chl_err = np.array(chl_err)
    chl_err = chl * chl_err/100
    #%
    t = pd.date_range('2009-06-01','2009-12-31',freq='d')
    fig = plt.figure(figsize=(10,3))
    gs = fig.add_gridspec(1,2)
    ax = fig.add_subplot(gs[0])
    def format_ax(ax):
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
        ax.tick_params(axis='x', labelrotation=0)
        ax.legend(fontsize=6)
        ax.grid(axis='x')
        ax.set_xlim('2009-06-01','2009-12-31')
        #ax.set_xticks(t)
        #ax.set_xlim(pd.to_datetime('2009-09-05'),pd.to_datetime('2009-10-15'))
    #LINKE SEITE:
    ax.plot(t,chl,color='#ff2e00',label='2009 Werte')
    ax.plot(t,cl_mean,label='Klima Mittelwert',color='#0037a1')
    ax.fill_between(t,cl_min,cl_max,label='3%/97% Perzentil',color='#13e3be',
        facecolor='#c1fbf6')
    ax.fill_between(t,chl-chl_err,chl+chl_err,
        color='#9d1c3f',facecolor='#fbe0f9',label='Geschätzter Fehler 2009')
    ax.fill_between(t,cl_mean-cl_std,cl_mean+cl_std,
        color='#0094ff',facecolor='#b0d9fb',label='Perzentil Std.abw.(16%/84%)',
        alpha=.5)
    format_ax(ax)
    ax.set_title('{:}° bis {:}° E und {:}° bis {:}° S\n({:}) Eintrag >{:.1f} ug/m2'.format(
        lon.start,lon.stop,lat.start*-1,lat.stop*-1,ort,tres))
    ax.set_ylabel('CHL-a Konzentrationen in mg/m3')
    #RECHTE SEITE:
    ax = fig.add_subplot(gs[1])
    ax.plot(t,chl-cl_mean,color='#ff2e00' ,label='Abweichungen zu Klimamittel')
    ax.fill_between(t,chl-cl_mean-chl_err,chl-cl_mean+chl_err,
        color='#9d1c3f',facecolor='#fbe0f9',label='Geschätzter Fehler 2009')
    ax.plot(t,np.zeros(t.size),color='black')
    ax.fill_between(t,-cl_std,cl_std,
        color='#0094ff',facecolor='#b0d9fb',label='Perzentil Std.abw.(16%/84%)',
        alpha=.5)
    format_ax(ax)
    ax.set_title('\nUm Trend bereinigt')
    plt.tight_layout()
    fig.savefig('D://thesisdata/Bilder/Python/wrf_chla/timeseries_'
        +ort+'_'+str(tres)+'ug.png',dpi=300)
    plt.close()
