import pandas as pd
import numpy as np

#pd.read_csv('./Python/air_quality/queensland_clean.csv')

path = '~/Downloads/'
file = '2009_victoria_air_quality.xls'

data = pd.read_excel(path+file)
data['sample_datetime'] = pd.to_datetime(data['sample_datetime'])
data = data.rename(columns={'sample_datetime':'time'})
data

new_aq = pd.DataFrame(columns=['value','time','variable','station','lon',
    'lat','region','site-id'])

new_aq[['value','time','variable','station','lon','lat']] = data[['PV','time',
    'param_id','sp_name','longitude','latitude']]
new_aq.replace('PPM2.5','PM2.5',inplace=True)

new_aq = (new_aq[(new_aq.variable=='PM10')|(new_aq.variable=='PM2.5')|
    (new_aq.variable=='API')])

set(new_aq.variable)

new_aq = new_aq.set_index('time')

new_aq.to_csv('./Python/air_quality/victoria_clean.csv')


import pandas as pd
nsw = pd.read_csv('./Python/air_quality/NSW_clean.csv')
queen = pd.read_csv('./Python/air_quality/queensland_clean.csv')
vic = pd.read_csv('./Python/air_quality/victoria_clean.csv')

nq = nsw.append(queen)
nqv = nq.append(vic)

nqv['time'] = pd.to_datetime(nqv['time'])
nqv = nqv.set_index('time')
nqv = nqv['2009-09-18':'2009-09-30']

nqv.to_csv('./Python/air_quality/clean.csv')

# test = pd.read_csv('./Python/air_quality/clean.csv',parse_dates=True,
#     index_col='time')
