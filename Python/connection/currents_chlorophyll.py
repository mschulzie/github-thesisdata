import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import helperlies as mway
import pandas as pd

chl_path = 'D://thesisdata/plankton/marine_copernicus/2005-2010_tasman_only.nc'
v_path = 'D://thesisdata/currents/global-reanalysis-phy-001-031-grepv2-mnstd-daily_2000_2010.nc'
v0 = xr.open_dataset(v_path).sel(time=slice('2005-01-01','2009-12-31'))
chl0 = xr.open_dataset(chl_path)
chl0=chl0['CHL']
#chl0.values = np.log10(chl0.values)
v0 = v0['vo_mean']
#%% CUT MONTHS:
start,end = '-09-01','-10-31'
v = v0.sel(time=slice('2005'+start,'2005'+end))
chl = chl0.sel(time=slice('2005'+start,'2005'+end))

for year in ['2006','2007','2008','2009']:
    v = xr.concat([v,v0.sel(time=slice(year+start,year+end))],dim='time')
    chl = xr.concat([chl,chl0.sel(time=slice(year+start,year+end))],dim='time')
#%%
v_ = v.mean(dim=('longitude','latitude')).values.flatten() - v.mean().values
chl_ = chl.mean(dim=('lon','lat')).values.flatten() - chl.mean().values
#%%
t = v.time.values
x_values = ['{:}'.format(x)[:10] for x in t]
len(x_values)
np.correlate(v_,chl_)

v_norm = v_ / v_.std()
chl_norm = chl_/chl_.std()
v_filt = mway.filter_via_fft(v_norm,freq_max=1/1)
chl_filt = mway.filter_via_fft(chl_norm,freq_max=1/1)

fig = plt.figure(figsize=(20,3))
ax = fig.add_subplot(111)
ax.plot(x_values,v_filt,label='v')
ax.plot(x_values,chl_filt,label='chl')
ax.set_xticks(['2005-09-01','2006-09-01','2007-09-01','2008-09-01','2009-09-01',
    '2005-10-01','2006-10-01','2007-10-01','2008-10-01','2009-10-01'])
ax.legend()
plt.show()
fig.savefig('corr_v_chl.png',dpi=500,bbox_inches='tight',pad_inches=0.01)
