import pandas as pd
import numpy as np


path = 'D://thesisdata/air_quality/Queensland/'
file1 = 'monitoring-sites-on-open-data.csv'
file2 = 'pm2-5-qld-2009.csv'
file3 = 'pm10-qld-2009.csv'
file4 = 'visibilityreducingparticles-qld-2009.csv'
#path = '/home/julchen/Studium/air_quality/New South Wales/PM_visibility.xls'
stations = pd.read_csv(path+file1,encoding='iso-8859-1',sep=';',decimal=',')
pm2 = pd.read_csv(path+file2,encoding='iso-8859-1')
pm10 = pd.read_csv(path+file3,encoding='iso-8859-1')
visi = pd.read_csv(path+file4,encoding='iso-8859-1')

v ={'PM2.5':pm2,'PM10':pm10,'visibility':visi}

for vari in v:
    for i in range(v[vari].shape[0]):
        time = v[vari]['Time'].values[i]
        date = v[vari]['Date'].values[i]
        v[vari].loc[i,'datetime'] = pd.to_datetime(date+' '+time)
    del v[vari]['Time']
    del v[vari]['Date']

stations

new_aq = pd.DataFrame(columns=['value','time','variable','station','lon',
    'lat','region','site-id'])
for vari in v:
    for col in v[vari].columns[:-1]:
        temp = pd.DataFrame(v[vari][col].values,columns=['value'])
        temp['time'] = v[vari]['datetime'].values
        temp['variable'] = vari
        temp['station'] = stations[stations.nameindata == col]['Site name'].values[0]
        temp['lon'] = stations[stations.nameindata == col]['Longitude'].values[0]
        temp['lat'] = stations[stations.nameindata == col]['Latitude'].values[0]
        temp['region']= ""
        temp['site-id']= ""
        new_aq = new_aq.append(temp)

new_aq = new_aq.set_index('time')
new_aq['2009-09']
new_aq.to_csv('./Python/air_quality/queensland_clean.csv')
