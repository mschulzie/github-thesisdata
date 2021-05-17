from warfy import Warfy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import helperlies as mway
import pandas as pd
import matplotlib.dates as mdates

path, savepath = mway.gimmedirs()

varname = 'DUSTLOAD'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]
data = Warfy()
data.load_var(var,file=path)
data.sum_vars(var,varname)
dust = data.get_var(varname)
dust_total = dust * mway.calc_qm(dust)
dust_time = dust_total.sum(dim=('lon','lat'))
dust.attrs
fig = plt.figure()
ax = fig.add_subplot(111)
dust_time.plot(ax=ax)
ticks = pd.date_range('2009-09-18T00','2009-09-30T00',freq='24H')
ax.set_xticks(ticks)
ax.set_xlim(pd.to_datetime('2009-09-18T00'),pd.to_datetime('2009-09-30T00'))
ax.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b - %H UTC'))

plt.show()
