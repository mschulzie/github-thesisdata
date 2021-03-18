import os

os.getcwd()

def gimmedirs():
    #haboob:
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
        print('Auf dem Laptop sind keine Daten du Troll!!!')

    else:
        print('Alter wo bist du denn? Am falschen PC?')
