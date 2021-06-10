import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

#just a comment

def gimmedirs():
    """
    Gibt Dir zwei Argumente zurück:
    return wrfout, savepic
    (Pfad der WRF-Datei auf deinem aktuellen Rechner
    und Pfad an dem die Bilder
    gespeichert werden sollen.)
    """
    #haboob (vergiss den Luder, der kannnix!):
    if (os.getcwd()=='/home/mschulz/atom'):
        print('Angemeldet auf haboob')
        wrfout = '/work/sulbrich/WRF-4.1.2/run/wrfout_d01_2009-09-18_00:00:00'
        savepic = '/home/mschulz/atom/pics/'
        return wrfout, savepic

    #Desktop-PC:
    elif (os.getcwd()=='C:\\Users\\mschu\\Documents\\Studium\\Bachelorarbeit\\github-thesisdata'):
        print('Angemeldet am Desktop-PC')
        wrfout = "D://thesisdata/wrf_dust/2021-06-09/wrfout_d01_2009-09-18_00_00_00"
        savepic = 'D://thesisdata/bilder/'
        return wrfout, savepic

    #Dektop-PC aber SSH-Ordner:
    elif (os.getcwd()=='Z:\\home\\mschulz\\github\\github-thesisdata'):
        print('Angemeldet am Desktop-PC ABER im SSH-Ordner, nutze wrfout auf HDD..')
        wrfout = "D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00"
        savepic = 'Z:\\home\\mschulz\\atom\\pics'
        return wrfout, savepic

    #Laptop Julchen:
    elif (os.getcwd()=='/home/julchen/github/github-thesisdata'):
        print('Auf dem Laptop sind jetzt Daten du Troll!!!')
        wrfout = "/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00"
        savepic = '/home/julchen/Bilder/'
        return wrfout, savepic
    else:
        print('Alter wo bist du denn? Am falschen PC?')

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
