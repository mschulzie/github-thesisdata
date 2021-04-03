import wrf
import xarray as xr
import netCDF4
import numpy as np
import wrfhelper_neu as wh
import matplotlib.pyplot as plt

file = '/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00'
#file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'
var = ['DUST_EMIS_ACC1','DUST_EMIS_ACC2','DUST_EMIS_ACC3','DUST_EMIS_ACC4','DUST_EMIS_ACC5']

test = wh.Warfy()
test.load_var(file,var)
test.sum_vars(var,'DUST_EMIS_ACC_SUM')
varr = test.get_var('DUST_EMIS_ACC_SUM')
maxvals = varr.max('time')

# N highest values:
N = 10

varr[maxvals.argmax(dim=('lon','lat'))].values[34]
maxvals[maxvals.argmax(dim=('lon','lat'))]
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(10):
    varr[maxvals.argmax(dim=('lon','lat'))].plot(ax=ax,label='test')
    maxvals[maxvals.argmax(dim=('lon','lat'))] = 0

ax.set_title('Timeseries of Maximum Values (DUST_EMIS_ACC_1-5)')
plt.legend()
plt.show()
