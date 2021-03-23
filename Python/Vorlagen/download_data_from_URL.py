import requests
import numpy as np
years = np.arange(2011,2018,1).tolist()
months = np.arange(1,8,1).tolist()

savedir = 'D://thesisdata/plankton/monthly/'

for year in years:
    for month in months:
        url = ('https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/'+
            'GMIS/satellite/9km/GMIS_A_CHLA_')
        string = str(month).zfill(2) +'_'+ str(year) + '.nc'
        url = url + string
        r = requests.get(url, allow_redirects=True)
        open(savedir+string, 'wb').write(r.content)
        
