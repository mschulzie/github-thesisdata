import os
#workDir = os.path.dirname(os.path.abspath(__file__))
workDir = 'D://thesisdata/plankton/cds_daily/'
os.chdir(workDir)
os.getcwd()
import numpy as np
import datetime as dt
import cdsapi

# =============================================================================
# Choose Download Parameters
# =============================================================================
dataset 	= 'satellite-ocean-colour'
variable 	= 'mass_concentration_of_chlorophyll_a'
projection = 'regular_latitude_longitude_grid'


years 		= [str(year) for year in np.arange(2016,2017)]
months 		= [str(month).zfill(2) for month in np.arange(10,12)]
days 		= [str(item).zfill(2) for item in np.arange(1,32)]

# =============================================================================
# Download CDS data
# =============================================================================
#%%
for year in sorted(years,reverse=True):
    for month in sorted(months,reverse=True):
        c = cdsapi.Client()

        c.retrieve(
            'satellite-ocean-colour',
            {
                'format': 'zip',
                'variable': variable,
                'year': year,
                'month': month,
                'day': days,
                'version': '5.0',
                'projection': projection,
            },
            year+month+variable+'.zip')
