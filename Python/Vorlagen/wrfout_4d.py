from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature
import wrf
import marcowhereareyou as mway

wrfout, savepic = mway.gimmedirs()
ncfile = Dataset(wrfout)
varname = "T"
plevel = 500.
var3d = wrf.getvar(ncfile,varname, timeidx=wrf.ALL_TIMES)
p = wrf.getvar(ncfile,"pressure",timeidx=wrf.ALL_TIMES)
#Computes the variables value at pressure level (interpolation):
var = wrf.interplevel(var3d, p, plevel)
var = var.isel(west_east=slice(0,143)) #damit 180° nicht überschritten
lats, lons = wrf.latlon_coords(var)
cart_proj = wrf.get_cartopy(var)
zeitpunkt = '2009-09-23T06'

#for zeitpunkt in var.coords['Time'].values: # dann plt.show() rausnehmen

fig = plt.figure(figsize=(12,6))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
ax.add_feature(cfeature.STATES,lw=.2, zorder=3)
plt.contourf(wrf.to_np(lons), wrf.to_np(lats),
            wrf.to_np(var.sel(Time=zeitpunkt)),
             zorder=4, transform=crs.PlateCarree(),
             cmap=get_cmap('RdBu_r'),alpha=1)
#cblevels = list(np.arange(0,1750e3,250e3))
cb=plt.colorbar(ax=ax, shrink=.98, label=(var3d.description+' in '+var3d.units))
#cb.set_ticks(cblevels)
ax.set_xlim(wrf.cartopy_xlim(var))
ax.set_ylim(wrf.cartopy_ylim(var))
# Add the gridlines
#ax.gridlines(color="black", linestyle="dotted")
gl = ax.gridlines(
    crs=crs.PlateCarree(), draw_labels=True,
    linewidth=1, color='gray', linestyle='dotted',
    xlocs=[120,135,150,165,180], zorder=6
    )
gl.top_labels = False
gl.right_labels = False

plt.title(str(zeitpunkt)[:13]+' - '+str(plevel)+' hPa')

fig.savefig(savepic+'Python/wrfout/'+varname+'/'+str(int(plevel))+'hPa/'
            +str(zeitpunkt)[:13]+'.png', dpi = 300)

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
