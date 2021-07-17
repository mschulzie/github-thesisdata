import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import helperlies as mway
import pandas as pd
from scipy.stats import pearsonr
#17.11.2000 und 18.11.2001 fehlen in CHL Daten!!! (WHY?!?!?)
#ENSO ??

chl_path = 'D://thesisdata/plankton/marine_copernicus/*_tasman_only.nc'
chl0
chl0 = xr.open_mfdataset(chl_path).sel(time=slice('2000-01-01','2019-12-31'))
chl0=chl0['CHL']
#chl0.values = np.log10(chl0.values)
#%% CUT MONTHS:
start,end = '-01-01','-12-31'
chl = chl0.sel(time=slice('2002'+start,'2002'+end))

for year in ['20{:}'.format(str(i).zfill(2)) for i in range(3,20)]:
    chl = xr.concat([chl,chl0.sel(time=slice(year+start,year+end))],dim='time')
#%%
chl_ = chl.mean(dim=('lon','lat')).values.flatten()# - chl.mean().values
#%% MAXIS:
maxis = ['2002-10-31',
 '2003-10-20',
 '2004-10-13',
 '2005-09-15',
 '2006-09-23',
 '2007-09-17',
 '2008-09-24',
 '2009-10-02',
 '2010-10-02',
 '2011-10-10',
 '2012-09-28',
 '2013-09-26',
 '2014-09-29',
 '2015-10-03',
 '2016-10-04',
 '2017-09-25',
 '2018-10-21',
 '2019-11-22']
 #%%
t = chl.time.values
x_values = ['{:}'.format(x)[:10] for x in t]

chl_norm = chl_/chl_.std()
chl_filt = mway.filter_via_fft(chl_,freq_max=1/180)

fig = plt.figure(figsize=(15,3))
ax = fig.add_subplot(111)
#ax.plot(x_values,v_filt,label='v')
ax.plot(x_values,chl_,label=r'$\mu_C(t)$ (155°-170°E; 30°-45°S)',
    color='#828282')
ax.plot(x_values,chl_filt,label=r'$\mu_C(t)$ gefiltert $f_\max$=2 p.a.',
    color='#0152db',linewidth=3)
ax.plot(x_values,mway.filter_via_fft(chl_,freq_max=1/1440),label=r'$\mu_C(t)$ gefiltert $f_\max$=1/4 p.a.',
    color='#ff6657',linewidth=3)
ticks = (['20{:}-09-01'.format(str(i).zfill(2)) for i in range(2,20)]+
    ['20{:}-09-01'.format(str(i).zfill(2)) for i in range(2,20)])
ax.set_xticks(maxis)
for label in ax.get_xticklabels():
  label.set_rotation(90)
  label.set_size(12)
ax.set_xlim(['2002-01-01','2019-31-12'])
ax.legend(loc='upper right')
ax.grid()
ax.set_ylabel('Chlorphyll-a in mg/m3',fontsize=12)
plt.show()
fig.savefig('./Thesis/bilder/long_timeseries_tasman.png',dpi=300,bbox_inches='tight',pad_inches=0.01)
#%% NINO:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def load_index(name, start='1950', end='2021'):
	df = pd.read_csv('./'+name+'.data',
	                   delim_whitespace=(1),skiprows=1, names=range(1,13))
	df = df.loc[start:end]
	df = df.astype(np.float64)
	df = df.stack()

	year = df.index.get_level_values(0).astype(int).values
	month = df.index.get_level_values(1).astype(int).values

	yearStart, yearEnd 		= [year[0], year[-1]]
	monthStart, monthEnd 	= [month[0], month[-1]]

	dateStart 	= str(yearStart) + '-' + str(monthStart)
	dateEnd 	= str(yearEnd) + '-' + str(monthEnd)

	df.index = pd.date_range(start=dateStart, end=dateEnd, freq='MS')

	return df

ds = load_index('oni')
xr_nino = xr.DataArray(ds['2002':'2020'].values,dims='time',coords={'time':ds['2002':'2020'].index})
nino = xr_nino.interp(coords=chl.drop(['lon','lat']).coords)

#%%
chl_n = (chl_-chl_.mean())/chl_.std()
coeffs = np.zeros(10000)

chl_fn = mway.filter_via_fft(chl_n,freq_max=1/180)
plt.plot(nino.time,nino)
plt.plot(nino.time,chl_fn)
pearsonr(chl_fn,nino.values)[0]
