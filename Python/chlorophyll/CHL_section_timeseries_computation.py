import xarray as xr
import helperlies as mway
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
import os
import string
tres = 5
kill_coast = False

from Python.modeloutput.deposition_iron import sections
# which= ['Tasman']#['Nordost','Korall','Tasman','Süden','Südozean']
# sections = {key: sections[key] for key in which}
#%%load var_names:
path = 'D://thesisdata/plankton/marine_copernicus/climatology/'
dir = os.listdir(path)
ds = xr.open_dataset(path+dir[0]).squeeze()
vars_cli = list(ds.variables)[3:]
path = 'D://thesisdata/plankton/marine_copernicus/2009/'
dir = os.listdir(path)
ds = xr.open_dataset(path+dir[0]).squeeze()
ds = ds.sel(lat=slice(-9.89,-57.06),lon=slice(110.3,189.7))
vars_2009 = list(ds.variables)[3:]
vars = vars_cli+vars_2009
add=''
mask = xr.open_dataset('D://thesisdata/wrf_dust/land_and_coast_mask.nc').sel(
    lon=slice(110,179),lat=slice(-57,-10))
sections
#%%
columns = []
for i,ort in enumerate(sections):
    for vari in vars:
        columns.append(ort+';'+vari)
        columns.append(ort+';'+vari+'_tres_'+str(tres))

data = pd.DataFrame(columns=columns)
data['time']= pd.date_range('2009-06-01','2009-12-31',freq='d')
#%% load iron:
data_iron = pd.DataFrame()
iron = mway.import_iron_dep(landmask=True,extend=['2009-06-01','2009-12-31'])
total_sum = iron.sum(dim='time') * 60 * 60 * 3
for ort in sections:
    data_iron[ort] = iron.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2])).mean(dim=('lon','lat')).values
data_iron['time'] = pd.date_range('2009-06-01','2009-12-31',freq='3h')
data_iron.to_csv('./Python/chlorophyll/csv/iron_section_means_timeseries.csv')
#%%
path = 'D://thesisdata/plankton/marine_copernicus/climatology/'

for l,file in enumerate(os.listdir(path)):
    ds = xr.open_dataset(path+file)
    #ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
    ds = ds.sel(lon=slice(110,179),lat=slice(-10,-57))
    ds = ds.interp(coords=mask.drop('time').coords)
    if kill_coast:
        ds = ds.where(mask['coast']==0)
    ds = ds.where(mask['land']==0)
    for ort in sections:
        for vari in vars_cli:
            total_sum_dt = total_sum.sel(lon=slice(sections[ort][0],sections[ort][1]),
                lat=slice(sections[ort][3],sections[ort][2]))
            dt = ds.sel(lon=slice(sections[ort][0],sections[ort][1]),
                lat=slice(sections[ort][3],sections[ort][2]))
            data.loc[l,ort+';'+vari] = dt[vari].mean(dim=('lon','lat')).values[0]
            dt = dt.where(total_sum_dt>tres)
            data.loc[l,ort+';'+vari+'_'+str(tres)] = dt[vari].mean(dim=('lon','lat')).values[0]
    if (np.mod(l,30)==0):
        print('climate timestep {:} finished'.format(l))

#% # Nun für 2009:
path = 'D://thesisdata/plankton/marine_copernicus/2009/'
for l,file in enumerate(os.listdir(path)):
    ds = xr.open_dataset(path+file)
    #ds = ds.assign_coords(lon=(ds.lon % 360)).roll(lon=(ds.dims['lon'] // 2), roll_coords=True)
    ds = ds.sel(lon=slice(110,179),lat=slice(-10,-57))
    ds = ds.interp(coords=mask.drop('time').coords)
    if kill_coast:
        ds = ds.where(mask['coast']==0)
    ds = ds.where(mask['land']==0)
    for ort in sections:
        for vari in vars_2009:
            total_sum_dt = total_sum.sel(lon=slice(sections[ort][0],sections[ort][1]),
                lat=slice(sections[ort][3],sections[ort][2]))
            dt = ds.sel(lon=slice(sections[ort][0],sections[ort][1]),
                lat=slice(sections[ort][3],sections[ort][2]))
            data.loc[l,ort+';'+vari] = dt[vari].mean(dim=('lon','lat')).values[0]
            dt = dt.where(total_sum_dt>tres)
            data.loc[l,ort+';'+vari+'_'+str(tres)] = dt[vari].mean(dim=('lon','lat')).values[0]
    if (np.mod(l,30)==0):
        print('2009 timestep {:} finished'.format(l))

for ort in sections:
    data[ort+';CHL_error'] = data[ort+';CHL']*data[ort+';CHL_error']/100
    data[ort+';CHL_error'+'_'+str(tres)] = data[ort+';CHL'+'_'+str(tres)]*data[ort+';CHL_error'+'_'+str(tres)]/100

if kill_coast==False:
    add+='_with_coast'
data.to_csv('./Python/chlorophyll/csv/chl_section_means_timeseries'+add+'.csv')
