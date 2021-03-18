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
# DAS HIER NUR AKTIVIEREN WENN WENN AUF BESTIMMTEN PLEVEL GEWÜNSCHT!
plevel = 950. # max 31
u_raw = wrf.getvar(ncfile,"ua",units="kt", timeidx=wrf.ALL_TIMES)
v_raw = wrf.getvar(ncfile,"va",units="kt", timeidx=wrf.ALL_TIMES)
wspd_raw = wrf.getvar(ncfile,"wspd_wdir",units="kts", timeidx=wrf.ALL_TIMES)[0,:]
p = wrf.getvar(ncfile,"pressure",timeidx=wrf.ALL_TIMES)

#Computes the variables value at pressure level (interpolation):
u = wrf.interplevel(u_raw, p, plevel).isel(west_east=slice(0,143))
v = wrf.interplevel(v_raw, p, plevel).isel(west_east=slice(0,143))
wspd = wrf.interplevel(wspd_raw, p, plevel).isel(west_east=slice(0,143))

#%%
#FALLS NUR WIND IN 10m Höhe gewünscht
# uv = wrf.getvar(ncfile,"uvmet10",units="kt",timeidx=wrf.ALL_TIMES).isel(
#                 west_east=slice(0,143))
#
# u = uv[0,:]
# v = uv[1,:]
# wspd= np.sqrt(u**2+v**2)

cart_proj = wrf.get_cartopy(u)
zeitpunkt = '2009-09-23T06'
levels= list(np.linspace(0,35,30))
lats, lons = wrf.latlon_coords(u)
#%%

#for zeitpunkt in u.coords['Time'].values: # dann plt.show() rausnehmen

fig = plt.figure(figsize=(12,6))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
ax.add_feature(cfeature.STATES,lw=.2, zorder=3)
wspd_contours = plt.contourf(wrf.to_np(lons), wrf.to_np(lats),
            wrf.to_np(wspd.sel(Time=zeitpunkt)),
             zorder=4, transform=crs.PlateCarree(),
             cmap=get_cmap('jet'),alpha=1,levels=levels,extend='max')
cb=plt.colorbar(wspd_contours, shrink=.98, label=(wspd_raw.description+
                            ' in '+u_raw.units))
cb.set_ticks(np.arange(0,36,5).tolist())
each = 8
plt.barbs(wrf.to_np(lons[::each,::each]), wrf.to_np(lats[::each,::each]),
            wrf.to_np(u.sel(Time=zeitpunkt)[::each,::each]),
            wrf.to_np(v.sel(Time=zeitpunkt)[::each,::each]),
             zorder=7, transform=crs.PlateCarree(), color="grey")

ax.set_xlim(wrf.cartopy_xlim(u))
ax.set_ylim(wrf.cartopy_ylim(u))
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

fig.savefig(savepic+'Python/wrfout/wind/'+str(int(plevel))+'hPa/'
     +str(zeitpunkt)[:13]+'.png', dpi = 300
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
