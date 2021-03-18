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
c = cdsapi.Client()

c.retrieve(
    dataset,
    {
        'format'		: 'zip',
        'variable'		: variable,
        'year'			: years,
        'projection'    : projection,
        'month'		    : month,
        'day' 			: days,
        'version'       : version,
    },
    workDir + filename)
