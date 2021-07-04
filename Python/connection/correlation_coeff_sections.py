import pandas as pd
from Python.modeloutput.deposition_iron import sections
import helperlies as mway
import warfy
import numpy as np

tau = 0

chl = pd.read_csv('./Python/chlorophyll/section_data_chl.csv',index_col='time',
    infer_datetime_format=True)
chl = chl.drop(columns=chl.columns[0])
d_chl = chl.diff()

dep = mway.import_iron_dep()
dep_ocean = dep.sel(time=slice('2009-09-18T03','2009-09-30T00'))
dep_day = dep_ocean.coarsen(time=8,boundary='exact',coord_func='max').mean(keep_attrs=True)
iron = pd.DataFrame()
iron['time'] = dep_day.time
iron = iron.set_index('time')
for ort in sections:
    dep_sec = dep_day.sel(lon=slice(sections[ort][0],sections[ort][1]),
        lat=slice(sections[ort][3],sections[ort][2]))
    iron[ort] = dep_sec.mean(dim=('lon','lat')).values
ext_time = pd.date_range('2009-10-01','2009-10-15',freq='d')
extension = pd.DataFrame(0,index=ext_time
    ,columns=iron.columns)
#iron = iron.append(extension)

def R_Fe_Chl(Fe,Chl,time,tau):
    N = time.size
    R_array=[]
    for t in tau:
        chl_start = time[0]+pd.DateOffset(days=int(t))
        chl_end = chl_start+pd.DateOffset(days=N-1)
        chl_start=str(chl_start)[:10]
        chl_end=str(chl_end)[:10]
        chl_shift = Chl[chl_start:chl_end]
        R = 1/N * np.sum(Fe.values * chl_shift.values)
        R = (R- Fe.values.mean()*chl_shift.values.mean())/(Fe.values.std()*chl_shift.values.std())
        R_array.append(R)
    return np.array(R_array)

tau = np.arange(15)
for ort in d_chl.columns:
    R = R_Fe_Chl(iron[ort],d_chl[ort],iron.index,tau)
    plt.plot(R)
    plt.show()
