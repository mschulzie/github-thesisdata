from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


from wrf import (to_np, getvar, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

ncfile = Dataset("D://thesisdata/wrf_dust/neu Sven/wrfout_d01_2009-09-18_00_00_00")
varname = "DUST_SOILFEDRYDEP_ACC_1"
i = 40
#for i in range(ncfile.dimensions['Time'].size): # dann plt.show() rausnehmen

var = getvar(ncfile,varname, timeidx=i)
fig = plt.figure(dpi=200)
ax1 = fig.add_subplot(1,1,1)
im = var.plot(ax=ax1, cmap='viridis')

fig.savefig(
            'D://thesisdata/bilder/Python/wrfout/'+varname+'/'
            +str(var.coords['Time'].values)[:13]+'.png', dpi = 300
            )
plt.show()
plt.close()


#SHAO's Variablenvorschläge:
#
#Wetter
# 1: 4-D Variablen, P, T, U, V, um Wetter darzustellen
#
# Dust in Atmosphäre
# 2: DUST_ACC_1 ... 5
#
# Dust Deposition und Emission und Load
# 3: 3-D Variablen DUSTLOAD_ACC1 ... 5
# 4: EDUST1 ... 5, DRYDEP_ACC1 ... 5, WETDEP_ACC1 ... 5
# 5: GRASET_ACC1 ... 5
#
# Danach analysieren wir die Fe Größen
# 6: DUST_SOILFE***_ACC1 ... 5.
