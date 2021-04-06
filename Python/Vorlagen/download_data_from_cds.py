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


#%%
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land',
    {
        'format': 'netcdf',
        'variable': [
            'lake_shape_factor', 'leaf_area_index_high_vegetation', 'leaf_area_index_low_vegetation',
            'skin_reservoir_content','volumetric_soil_water_layer_1','volumetric_soil_water_layer_2'
            ,'volumetric_soil_water_layer_3','volumetric_soil_water_layer_4',
            'skin_temperature'
        ],
        'year': '2009',
        'month': '09',
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            -10, 112, -40,
            155,
        ],
    },
    'D://thesisdata/soil_moisture/ERA5-Land_hourly.nc')
