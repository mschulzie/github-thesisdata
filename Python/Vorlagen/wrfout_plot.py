from netCDF4 import Dataset
import marcowhereareyou as mway
import wrfhelper as wrfhelp

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)


var = wrfhelp.wrfplot(wrffile,'DUSTLOAD_4',
                compare_var='RAINC',
                ppfig=(1,1),
                time='2009-09-23T12',
                cmap='plasma',
                show=True,
                #save=True,
                savedir=savedir,
                qmin=0,
                #qmax=0.95,
                limmax=1001 #suppresses qmax!!!
                #levels=11
                )
