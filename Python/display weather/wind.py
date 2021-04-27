import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import os
import helperlies as mway

#convert time steps to those in WRF-output
wind = xr.open_dataset('D://thesisdata/weather_stuff/uv_t_msl_tp_slh.nc')
time='2009-09-22T01'
wind = wind.sel(time=time)
u = wind['u10']
v = wind['v10']
speed = np.sqrt(u**2+v**2) * 3.6 / 1.852 # in knots
# tp = tp['tp']
# tp = tp.sel(time=slice('2009-09-01T01','2009-09-30T21')).coarsen(time=3,
#     keep_attrs=True).sum()
# tp['time'] = pd.date_range("2009-09-01T03", freq="3H", periods=239)
# #convert to mm:
# tp.attrs['units'] = 'mm'
# tp.attrs['long_name'] = 'Total precipitation (acc. last 3h)'
# tp.values = tp*1000

#%%
#Plotting:

# tp = tp.sel(time=slice('2009-09-18T00','2009-09-30T00'))
#
# for dt in tp.time.values:

#c_levels = np.linspace(1,37,50)
fig = plt.figure(figsize=(5,3.2))
gs = fig.add_gridspec(1,1,hspace=0.4)
ax = fig.add_subplot(gs[0,0], projection=crs.Mercator(
    central_longitude=150.0))

ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=1)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=0)
ax.add_feature(cfeature.STATES,lw=.2, zorder=1)

scale = 10
levels = np.arange(0,45,5).tolist()
LON, LAT = np.meshgrid(u.longitude.values, u.latitude.values)
vec = ax.quiver(LON[::scale,::scale], LAT[::scale,::scale],u.values[::scale,::scale],v.values[::scale,::scale],
    transform=crs.PlateCarree(), zorder = 2)
cont = ax.contourf(LON,LAT,speed, transform=crs.PlateCarree(),
    zorder=1,cmap='jet',alpha=.8, levels=levels,extend='max')


cb = plt.colorbar(cont, shrink=.98,format='%d')
cb.set_label('10m Wind in Knoten',fontsize=8)

ax.set_extent([110,189,-9,-57],crs=crs.PlateCarree())
ax.set_title(time+'- ERA-5')
#ax.set_ylim(wrf.cartopy_ylim(var))
gl = ax.gridlines(
    crs=crs.PlateCarree(),
    draw_labels=True,
    linewidth=1, color='gray', linestyle='dotted',
    zorder=4)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# cities = mway.loadcities()
# for city in cities:
#     ax.text(cities[city][0]+.1,cities[city][1]+.1,
#         city,fontsize=2,
#         zorder=8,transform=crs.PlateCarree(),ha='left')
#     ax.plot(cities[city][0],cities[city][1],color='red',
#         zorder=7,transform=crs.PlateCarree(),
#         marker='o',markersize=.2)

fig.savefig('D://thesisdata/bilder/Python/era5/wind/'+time+'.png',
    dpi=500)
