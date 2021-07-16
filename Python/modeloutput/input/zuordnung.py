
import pandas as pd
soils_full = pd.read_csv('./Python/modeloutput/input/SOILPARM.TBL',skiprows=3,
    sep=',',header=None)
soils = soils_full.loc[:18,[0,11]]
soils.columns=['Ziffer','Bezeichnung']
#%%
landuse_full=pd.read_csv('./Python/modeloutput/input/LANDUSE.TBL',skiprows=33,
    sep=',',header=None)
landuse=landuse_full.loc[:32,[0,8]]
landuse.columns=['Ziffer','Bezeichnung']
#%%
soils['colors'] = ['#ffffed','#eef093','#ff8200','#903400',
    '#f7643d','#cfa15e','#0d6502','#3d44ab',
    '#404040','#b400ff','#0044ff','#ff0000',
    '#343434','#a3caf7','#444444','#6a0d0d',
    '#ffffff','#ffffff','#ffffff'
    ]

landuse['colors'] = ['#ff0000','#6a3a01','#2b18ff','#903400',
    '#f7643d','#ff59fd','#0d6502','#ffc188',
    '#fdffa3','#90a367','#0044ff','#7993ff',
    '#003804','#a3caf7','#ff7a00','#a3caf7',
    '#d0d0d0','#ffffff','#ffffff','#ffffff',
    '#ffffff','#ffffff','#ffffff','#ffffff',
    '#ffffff','#ffffff','#ffffff','#ffffff',
    '#ffffff','#ffffff','#ffffff','#ffffff',
    '#eeba0f'
    ]

txt = pd.read_csv('./Python/modeloutput/input/txt.txt',header=None)
txt2 = pd.read_csv('./Python/modeloutput/input/txt2.txt',header=None)
soils['Bez. Deutsch'] = txt
landuse['Bez. Deutsch'] = txt2
