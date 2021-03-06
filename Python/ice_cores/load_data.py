import pandas as pd
import requests
import numpy as np

savedir = 'D://thesisdata/ice_cores/'

url = ('https://www.ncei.noaa.gov/pub/data/paleo/icecore/'+
    'antarctica/epica_domec/')
data = 'edc2012dust.txt'

r = requests.get(url+data, allow_redirects=True)
open(savedir+data, 'wb').write(r.content)
