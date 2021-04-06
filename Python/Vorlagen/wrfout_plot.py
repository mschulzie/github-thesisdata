from netCDF4 import Dataset
import helperlies as mway
import wrfhelper as wrfhelp

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)

cities=mway.loadcities()

var = wrfhelp.wrfplot(wrffile,'DUST_EMIS_ACC',
                #compare_var='DUST_EMIS_ACC',
                lons = (140,141.5),
                lats = (-25,-22),
                #ppfig=(4,4),
                #time='2009-09-18T12',
                time=slice('2009-09-18T00','2009-09-30T00'),
                cmap='jet',
                show=True,
                save=True,
                savedir=savedir,
                #qmin=0.1,
                #qmax=1,
                #limmin=1, #suppresses qmin!!!
                #limmax=2e6, #suppresses qmax!!!
                #levels=[1,20,100,1000,1e4,1e5,1e6,1e7],
                zlevel=0, # zlevel ranges from 0 to 31 (32 levels)
                contour_color=['#00fff7','#2af268','#0019fc'],
                #contour_levels=5,
                only_maxvals = True,
                cities=cities
                )

var.shape

#Nur Variable über alle Zeiten angucken:
#var,_,_,_,_ = wrfhelp.loadvar(wrffile,'DUST_ACC_',zlevel=1)
