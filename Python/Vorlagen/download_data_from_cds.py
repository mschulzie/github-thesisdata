#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created by  : Niclas Rieger
# Created on  : Mon Janu 18 19:35 2021
# =============================================================================
""" Download Ocean colour daily from ECMWF """
# =============================================================================
# Imports
# =============================================================================
import os
#workDir = os.path.dirname(os.path.abspath(__file__))
workDir = 'D://thesisdata/plankton/'
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
#               'remote_sensing_reflectance',

projection = 'regular_latitude_longitude_grid'
#             'sinusoidal_grid'

years 		= '2009'
month 		= '11'
days 		= [str(item).zfill(2) for item in np.arange(1,32).tolist()]
version     = '5.0' # '3.1' '4.2'
# time steps are often only '00:00' for daily accumulated or monthly means
# options: eg. 0.25, 0.5, 1.0
area 		= [-5, -180, -60, 180]
# full globe: [90, -180, -90, 180]

filename 	= dataset +'_'+variable+'_'+month+'_'+years
# =============================================================================
# Download CDS data
# =============================================================================
#%%
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind',
            '2m_temperature', 'mean_sea_level_pressure',
            'total_precipitation','significant_height_of_combined_wind_waves_and_swell',
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
            -9, -180, -60,
            -170,
        ],
    },
    'download.nc')
