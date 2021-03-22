from netCDF4 import Dataset
import marcowhereareyou as mway
import wrfhelper as wrfhelp

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)

var = wrfhelp.wrfplot(wrffile,'DUSTLOAD_',
                #compare_var='RAIN',
                #lons = (145,175),
                #lats = (-50,-25),
                #ppfig=(4,2),
                time=slice('2009-09-18T00','2009-09-30T00'),
                #time='2009-09-24T00',
                cmap='YlOrBr',
                show=False,
                save=True,
                savedir=savedir,
                #qmin=0.9,
                #qmax=1,
                limmin=1e4, #suppresses qmin!!!
                limmax=1e6, #suppresses qmax!!!
                #levels=11,
                #zlevel=0, # zlevel ranges from 0 to 31 (32 levels)
                contour_color=['#0d00ff','#2ac8f2','#75bfff'],
                #contour_levels=10
                )

#Nur Variable über alle Zeiten angucken:
#var,_,_,_,_ = wrfhelp.loadvar(wrffile,'PREC_ACC_NC')
