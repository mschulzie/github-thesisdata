import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from warfy import Warfy
import xarray as xr
import pandas as pd

def gimmedirs():
    """
    Gibt Dir zwei Argumente zurück:
    return wrfout, savepic
    (Pfad der WRF-Datei auf deinem aktuellen Rechner
    und Pfad an dem die Bilder
    gespeichert werden sollen.)
    """
    wrfout = "D://thesisdata/wrf_dust/2021-06-09/wrfout_d01_2009-09-18_00_00_00"
    savepic = 'D://thesisdata/bilder/'
    return wrfout, savepic

def show_nan(data_array,time=slice('1990','2099')):
    """
    Plots a lon-lat contour to show the percentage of nan-values
    values in a 3D xarray. Requires time.size > 1.
    You may put in the desired time range as a slice object.
    """
    ds = data_array.sel(time=time)
    nan_percentage = 100*(ds.time.size - ds.count(dim='time')) / ds.time.size
    im = nan_percentage.plot(cmap='magma_r',levels=11,extend='max',
        add_colorbar=False)
    plt.title(str(ds.time.values[0])[:10]+' to '+
        str(ds.time.values[-1])[:10]
        +' ('+str(ds.time.size)+' timesteps)')
    cb = plt.colorbar(im,label='Percentage of NaN Values')
    cb.set_ticks(np.arange(0,110,10).tolist())
    cb.set_ticklabels([str(x)+'%' for x in np.arange(0,110,10)])
    return

def loadcities():
    cities = {
      "Sydney": [151.2,-33.8],
      #"Canberra": [149.1,-35.3],
      "Diamantara Lakes": [141.2,-23.9],
      "Boulia": [139.9,-22.9],
      "Mount Isa City": [139.5,-20.7],
      "Darwin": [130.8,-12.5],
      "Brisbane": [153.0,-27.5],
      'Newcastle': [151.8,-32.9],
      'Albion Park': [150.78,-34.58],
      #'Bathurst' : [149.58,-33.42],
      'Wagga Wagga': [147.36,-35.11],
      'Kati Thanda-Lake Eyre': [137.95,-28.3]
    }
    return cities

def make_segmented_cmap(*colors):
    if len(colors)==0:
        colors =  ('#000303','#750b2e','#f7f7f7','#066479','#000303')
    anglemap = LinearSegmentedColormap.from_list(
        'anglemap', np.array(colors), N=256, gamma=1
        )
    return anglemap

phase = make_segmented_cmap(
    '#d62323','#b4622d','#1473c1','#471d70','#d62323')


def calc_qm(xarray):
    f = (6378.137e3-6356.752314e3)/6378.137e3 # Abplattung
    diffphi = np.radians(np.append(np.diff(xarray['lon'].values),np.diff(xarray['lon'].values)[-1]))
    difftheta = np.radians(np.append(np.diff(xarray['lat'].values),np.diff(xarray['lat'].values)[-1]))

    LON,LAT = np.meshgrid(xarray['lon'].values,xarray['lat'].values)
    PHI = np.radians(LON)
    THETA = np.radians((LAT - 90)*-1)
    DIFFPHI,DIFFTHETA = np.meshgrid(diffphi,difftheta)
    R = 6378.137e3*(1-f*np.cos(DIFFTHETA)**2)
    QM = R**2 * (DIFFPHI *(np.cos(THETA-DIFFTHETA/2)-np.cos(THETA+DIFFTHETA/2)))
    return QM

def grid_distances(xarray):
    """
    Return two xarrays lon_distance, lat_distance containing the distances
    to the neighboured grid points for each grid point
    """
    f = (6378.137e3-6356.752314e3)/6378.137e3 # Abplattung
    diffphi = np.radians(np.append(np.diff(xarray['lon'].values),np.diff(xarray['lon'].values)[-1]))
    difftheta = np.radians(np.append(np.diff(xarray['lat'].values),np.diff(xarray['lat'].values)[-1]))

    LON,LAT = np.meshgrid(xarray['lon'].values,xarray['lat'].values)
    PHI = np.radians(LON)
    THETA = np.radians((LAT - 90)*-1)
    DIFFPHI,DIFFTHETA = np.meshgrid(diffphi,difftheta)
    R = 6378.137e3*(1-f*np.cos(DIFFTHETA)**2)
    lon_distance = R * DIFFPHI * np.sin(THETA)
    lat_distance = R * DIFFTHETA
    lon_distance = xr.DataArray(lon_distance,coords={'lat':xarray.lat.values,
        'lon':xarray.lon.values},dims=['lat','lon'])
    lat_distance = xr.DataArray(lat_distance,coords={'lat':xarray.lat.values,
        'lon':xarray.lon.values},dims=['lat','lon'])
    return lon_distance, lat_distance

def argmax_array(array,N):
    """
    Returns array with N highest values, Rest as NaN
    """
    dummy = array.copy(deep=True)
    mask = array.where(array<array.min())
    for i in range(N):
        value = dummy[dummy.argmax(dim=('lon','lat'))].values
        if value != 0:
            mask[dummy.argmax(dim=('lon','lat'))] = value
            dummy[dummy.argmax(dim=('lon','lat'))] = 0
    return array.where(mask.values==array.values)
def argmax_n(array,n):
    """
    Returns n-th max values coordinates
    """
    dummy = array.copy(deep=True)
    for i in range(n-1):
        value = dummy[dummy.argmax(dim=('lon','lat'))].values
        if value != 0:
            dummy[dummy.argmax(dim=('lon','lat'))] = 0
    return dummy.argmax(dim=('lon','lat'))

def box_to_plot(box):
    x = [box[0],box[1],box[1],box[0],box[0]]
    y = [box[2],box[2],box[3],box[3],box[2]]
    return x, y

def nM_to_ug_per_qm(c,z=1):
    M_Fe = 55.845 /1000 # in kg pro Mol
    c = c*1e-9 * 1e3
    return c * z * M_Fe * 1e9 # in ug pro qm
def ug_per_qm_to_nM(F,z=1):
    M_Fe = 55.845
    return F/z*1e-9/M_Fe*1e9

def import_iron_dep(landmask=True,extend=['2009-09-18T00','2009-09-30T00']):
    #options = ['WETDEP_ACC','GRASET_ACC','DRYDEP_ACC']
    options = ['DUST_SOILFEWETDEP_ACC','DUST_SOILFEGRASET_ACC','DUST_SOILFEDRYDEP_ACC']
    wet_name= options[0]
    gra_name= options[1]
    dry_name= options[2]
    liste = [wet_name,gra_name,dry_name]
    j = 0
    for var in liste:
        var = [var]*5
        var = [var[i]+'_'+str(i+1) for i in range(5)]
        liste[j] = var
        j+=1
    wet = Warfy()
    wet.load_var(liste[0])
    wet.sum_vars(liste[0],wet_name)
    wet = wet.get_var(wet_name)
    gra = Warfy()
    gra.load_var(liste[1])
    gra.sum_vars(liste[1],gra_name)
    gra = gra.get_var(gra_name)
    dry = Warfy()
    dry.load_var(liste[2])
    dry.sum_vars(liste[2],dry_name)
    dry = dry.get_var(dry_name)
    gra.values[gra.values<0] = gra.values[gra.values<0] * -1
    dry.values[dry.values<0] = dry.values[dry.values<0] * -1
    total = xr.DataArray(gra.values+wet.values+dry.values,
        coords=wet.coords,dims=wet.dims,attrs=wet.attrs)
    total.attrs['description'] ='Total dust deposition rate all binsizes'
    if extend!=['2009-09-18T00','2009-09-30T00']:
        iron_add_start = xr.DataArray(np.zeros((pd.date_range(extend[0],
            '2009-09-17T21',freq='3h').size,)+total.shape[1:]),dims=total.dims,
            coords={'time':pd.date_range(extend[0],'2009-09-17T21',freq='3h'),
            'lat':total.lat.values,'lon':total.lon.values})
        iron_add_end = xr.DataArray(np.zeros((pd.date_range('2009-09-30T03',
            extend[1],freq='3h').size,)+total.shape[1:]),dims=total.dims,
            coords={'time':pd.date_range('2009-09-30T03',extend[1],freq='3h'),
            'lat':total.lat.values,'lon':total.lon.values})
        total = xr.concat((iron_add_start,total,iron_add_end),dim='time')
    if landmask == True:
        land = Warfy()
        land.load_var('LANDMASK')
        mask = land.get_var('LANDMASK').isel(time=0)
        total = total.where(mask==0)
    return total

def filter_via_fft(signal,freq_max=None,freq_min=None):
    """
    returns filtered signal
    freq_max and freq_min in multiples of given sample rate of signal!
    (if daily data: freq_max=1/10 means eliminating all frequencies
    higher then "every 10th day")
    """
    fhat = np.fft.fft(signal)
    freq = np.fft.fftfreq(signal.size,1)
    fhat_new = np.zeros(fhat.size,dtype='complex')
    if ((freq_max!=None) & (freq_min!=None)):
        fhat_new[(abs(freq)<=freq_max)&(abs(freq)>=freq_min)] = fhat[(abs(freq)<=freq_max)&(abs(freq)>=freq_min)]
    elif (freq_max!=None):
        fhat_new[abs(freq)<=freq_max] = fhat[abs(freq)<=freq_max]
    elif freq_min!=None:
        fhat_new[abs(freq)>=freq_min] = fhat[abs(freq)>=freq_min]
    else:
        fhat_new = fhat
        print('Nothing happened... Damn.. Provide limits!!')

    signal_filter = np.fft.ifft(fhat_new)
    signal_filter = signal_filter.real
    return signal_filter
