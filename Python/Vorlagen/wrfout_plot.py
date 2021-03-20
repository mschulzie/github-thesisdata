from netCDF4 import Dataset
import marcowhereareyou as mway
import wrfhelper as wrfhelp

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)


var = wrfhelp.wrfplot(wrffile,'RAIN',
                #compare_var='RAINC',
                ppfig=(1,1),
                #time=slice('2009-09-23T12','2009-09-24T09'),
                time='2009-09-19T12',
                cmap='Blues',
                show=True,
                save=True,
                savedir=savedir,
                #qmin=0,
                #qmax=1,
                limmax=72 #suppresses qmax!!!
                #levels=11
                )

var.shape
var.sel(south_north=slice(0,124)).plot()
