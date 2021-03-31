import pandas as pd
import os

pathcoords = './Python/air_quality/dustwatch_coords.csv'
coords = pd.read_csv(pathcoords,decimal=',',sep=';')
txtcol = 'Location Dataset (homogenized)'
coords
path = 'D://thesisdata/DUST_OBS/DUSTWATCH/observations_homogenized/'
dw = pd.DataFrame(columns=['time','value','variable','station','lon','lat',
    'region','site-id','datasource'])
for file in os.listdir(path):
    txt_ = pd.DataFrame(columns=dw.columns)
    txt = pd.read_csv(path+file,sep='\t',header=[0,1],parse_dates=True,
        index_col=0)
    txt = txt['2009-09-18':'2009-09-30']
    txt_['time'] = txt.index
    txt_['value'] = txt.iloc[:,0].values
    txt_['variable'] = 'DUST /Fog.Smoke removed'
    txt_['datasource'] = 'DustWatch'
    txt_['station'] = coords[coords[txtcol]==file]['Location Detail'].values[0]
    txt_['lon'] = coords[coords[txtcol]==file].Longitude.values[0]
    txt_['lat'] = coords[coords[txtcol]==file].Latitude.values[0]
    txt_['site-id'] = coords[coords[txtcol]==file]['Site ID'].values[0]
    dw = dw.append(txt_)

dw = dw.set_index('time')
dw.to_csv('./Python/air_quality/dustwatch_data.csv')
