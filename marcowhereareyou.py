import os
import matplotlib.pyplot as plt
import numpy as np

#just a comment

os.getcwd()

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
        wrfout = "D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00"
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
