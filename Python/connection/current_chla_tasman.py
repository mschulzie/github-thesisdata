import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import helperlies as mway
import pandas as pd
from scipy.stats import pearsonr
#17.11.2000 und 18.11.2001 fehlen in CHL Daten!!! (WHY?!?!?)
#ENSO ??

chl_path = 'D://thesisdata/plankton/marine_copernicus/*_tasman_only.nc'
v_path = 'D://thesisdata/currents/2000-2019_tasman_south_only.nc'
v0 = xr.open_dataset(v_path).sel(latitude=slice(-50,-40))
chl0 = xr.open_mfdataset(chl_path).sel(time=slice('2000-01-01','2019-12-31'))
chl0=chl0['CHL']
#chl0.values = np.log10(chl0.values)
v0 = v0['vo_mean']
#%% CUT MONTHS:
start,end = '-09-01','-10-31'
v = v0.sel(time=slice('2002'+start,'2002'+end))
chl = chl0.sel(time=slice('2002'+start,'2002'+end))

for year in ['20{:}'.format(str(i).zfill(2)) for i in range(3,20)]:
    v = xr.concat([v,v0.sel(time=slice(year+start,year+end))],dim='time')
    chl = xr.concat([chl,chl0.sel(time=slice(year+start,year+end))],dim='time')
#%%
v_ = v.mean(dim=('longitude','latitude')).values.flatten() - v.mean().values
chl_ = chl.mean(dim=('lon','lat')).values.flatten() - chl.mean().values
 #%%
t = chl.time.values
x_values = ['{:}'.format(x)[:10] for x in t]

pearsonr(v_[:-5],chl_[5:])

v_norm = v_ / v_.std()
chl_norm = chl_/chl_.std()
v_filt = mway.filter_via_fft(v_norm,freq_max=1/1)
chl_filt = mway.filter_via_fft(chl_norm,freq_max=1/1)
v_diff = abs(np.diff(v_filt))
chl_diff = abs(np.diff(chl_filt))
fig = plt.figure(figsize=(15,3))
ax = fig.add_subplot(111)
ax.plot(x_values[1:],v_diff,label=r'$\Delta \mu_v(t)$')
ax.plot(x_values[1:],chl_diff,label=r'$\Delta \mu_C(t)$ (155°-170°E; 30°-45°S)',
    color='#828282')
ticks = (['20{:}-09-01'.format(str(i).zfill(2)) for i in range(2,20)]+
    ['20{:}-10-01'.format(str(i).zfill(2)) for i in range(2,20)])
ax.set_xticks(ticks)

for label in ax.get_xticklabels():
  label.set_rotation(90)
  label.set_size(12)
ax.set_xlim(['2002-09-02','2019-10-31'])
ax.legend(loc='upper right')
ax.grid()
ax.set_ylabel('Chlorphyll-a / Strömung v (normalisiert)',fontsize=12)
plt.show()
fig.savefig('./Thesis/bilder/current_chla_tasman.png',dpi=300,bbox_inches='tight',pad_inches=0.01)
