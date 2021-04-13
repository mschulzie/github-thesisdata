import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

path = 'D://thesisdata/ice_cores/'

dome_co2 = pd.read_csv(path+'edc-co2-2008_composite.txt',
    header=91,delim_whitespace=True).set_index('Age(yrBP)')

dome_dust = pd.read_csv(path+'edc-dust2008_clean.txt',
    header=6,delim_whitespace=True).set_index('EDC3Age(kyrBP)').drop(
    columns='Depth(m)')

dome_ch4 = pd.read_csv(path+'edc-ch4-2008_clean.txt',
    header=0,delim_whitespace=True).set_index('Gas_Age').drop(
    columns=['Depth','Lab.','1s'])

dome_temp = pd.read_csv(path+'edc3deuttemp2007_clean.txt',
    header=0,delim_whitespace=True)
dome_temp
dome_ch4.plot()


# dome_temp DOWNLOAD klappt derzeit nicht!!
