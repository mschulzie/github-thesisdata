from warfy import Warfy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import helperlies as mway

varname = 'DUSTLOAD'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]
data = Warfy()
data.load_var(var)
data.sum_vars(var,varname)
dust = data.get_var(varname)
dust_total = dust * mway.calc_qm(dust)
dust_time = dust_total.sum(dim=('lon','lat'))
dust_time.plot()
