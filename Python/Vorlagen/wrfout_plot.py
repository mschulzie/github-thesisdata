from netCDF4 import Dataset
import marcowhereareyou as mway
import wrfhelper as wrfhelp
from cities import loadcities

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)

cities=loadcities()

var = wrfhelp.wrfplot(wrffile,'RAIN',
                #compare_var='RAIN',
                #lons = (0,155),
                #lats = (-40,0),
                #ppfig=(4,4),
                time=slice('2009-09-18T00','2009-09-30T00'),
                cmap='winter',
                show=True,
                save=True,
                savedir=savedir,
                #qmin=0.1,
                #qmax=1,
                limmin=1, #suppresses qmin!!!
                #limmax=5, #suppresses qmax!!!
                #levels=10,
                #zlevel=0, # zlevel ranges from 0 to 31 (32 levels)
                contour_color=['#0d00ff','#2ac8f2','#75bfff'],
                #contour_levels=10,
                #only_maxvals = True,
                cities=cities
                )

#Nur Variable über alle Zeiten angucken:
#var,_,_,_,_ = wrfhelp.loadvar(wrffile,'PREC_ACC_NC')
