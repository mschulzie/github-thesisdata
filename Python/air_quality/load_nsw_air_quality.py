import pandas as pd
import numpy as np

path = 'D://thesisdata/air_quality/New South Wales/PM_visibility.xls'
aq = pd.read_excel(path,header=2)
aq
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
aq = aq.set_index('datetime')

aq
aq['2009-09-23':'2009-09-27']['RANDWICK']['PM10'].plot(title='Test')

var = pd.read_json('./Python/air_quality/get_SiteDetails.json')

var[var['SiteName']=='LIVERPOOL'].Longitude.values
