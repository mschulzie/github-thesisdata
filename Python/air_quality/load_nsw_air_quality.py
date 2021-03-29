import pandas as pd
import numpy as np


path = 'D://thesisdata/air_quality/New South Wales/PM_visibility.xls'
#path = '/home/julchen/Studium/air_quality/New South Wales/PM_visibility.xls'
aq = pd.read_excel(path,header=2)
parameters = ['PM2.5','NEPH','PM10']
for p in parameters:
    stations = []
    for col in aq.columns:
        if (col.find(p) >= 0):
            stations.append(col[:col.find(p)-1])
    print(str(len(stations))+' stations with parameter '+p)

second_header = ['Date','Time']
for col in aq.columns:
    for p in parameters:
        if (col.find(p) >= 0):
            second_header.append(col[:col.find(p)-1])
            aq.rename(columns={col:col[col.find(p):col.find(p)+len(p)]},
                inplace=True)
if (len(second_header) != aq.shape[1]):
    raise ValueError('Can not create second header row.'+
        'Some parameters missing or doubled?')
cols = list(zip(second_header,aq.columns))
aq.columns = pd.MultiIndex.from_tuples(cols)
#replace bad time format 24:00 to 00:00:
for i in range(aq.shape[0]):
    time = aq['Time'].values[i]
    date = aq['Date'].values[i]
    offset = 0
    if time == '24:00':
        time = '00:00'
        offset = 1
    aq.loc[i,'datetime'] = (pd.to_datetime(date+' '+time)
        + pd.DateOffset(days=offset))
del aq['Time']
del aq['Date']
#aq = aq.set_index('datetime')
stations = pd.read_json('./Python/air_quality/get_SiteDetails.json')
new_aq = pd.DataFrame(columns=['value','time','variable','station','lon',
    'lat','region','site-id'])

for col in aq.columns[:-1]:
    temp = pd.DataFrame(aq[col].values,columns=['value'])
    temp['time'] = aq['datetime'].values
    temp['variable'] = col[1]
    temp['station'] = col[0]
    temp['lon'] = stations[stations.SiteName == col[0]]['Longitude'].values[0]
    temp['lat'] = stations[stations.SiteName == col[0]]['Latitude'].values[0]
    temp['region']= stations[stations.SiteName == col[0]]['Region'].values[0]
    temp['site-id']= stations[stations.SiteName == col[0]]['Site_Id'].values[0]
    new_aq = new_aq.append(temp)

new_aq = new_aq.set_index('time')
new_aq.to_csv('./Python/air_quality/NSW_clean.csv')
