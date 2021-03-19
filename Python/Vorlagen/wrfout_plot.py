from netCDF4 import Dataset
import marcowhereareyou as mway
import wrfhelper as wrfhelp

wrfout, savedir = mway.gimmedirs()
wrffile = Dataset(wrfout)


wrfhelp.wrfplot(wrffile,'RAINC',
                ppfig=(4,2),
                time=slice('2009-09-23T12','2009-09-24T09'),
                cmap='Blues',
                show=True,
                save=True,
                savedir=savedir)
