from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature
import wrf
import matplotlib.image as mpimg

ncfile = Dataset("D://thesisdata/wrf_dust/neu Sven/wrfout_d01_2009-09-18_00_00_00")
uv = wrf.getvar(ncfile,"uvmet10",units="kt",timeidx=wrf.ALL_TIMES).isel(
                west_east=slice(0,143))

u = uv[0,:]
v = uv[1,:]
wspd= np.sqrt(u**2+v**2)
levels= list(np.linspace(0,35,30))
lats, lons = wrf.latlon_coords(u)
cart_proj = wrf.get_cartopy(u)
zeitpunkt = '2009-09-23T06'
#%%

#for zeitpunkt in u.coords['Time'].values[::2]: # dann plt.show() rausnehmen

fig = plt.figure(figsize=(12,6))
widths = [18,15,1]
gs = fig.add_gridspec(1, 3,width_ratios=widths,wspace=0.05)
# Set the GeoAxes to the projection used by WRF
ax = fig.add_subplot(gs[0,0], projection=cart_proj)
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
ax.add_feature(cfeature.STATES,lw=.2, zorder=3)
wspd_contours = plt.contourf(wrf.to_np(lons), wrf.to_np(lats),
            wrf.to_np(wspd.sel(Time=zeitpunkt)),
             zorder=4, transform=crs.PlateCarree(),
             cmap=get_cmap('jet'),alpha=1,levels=levels,extend='max')
cb=plt.colorbar(wspd_contours, shrink=.6, label=(u.description+
                            ' in '+u.units))
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
zeitstr = str(zeitpunkt)
ax.set_title('WRF - '+zeitstr[:13])#+' - '+str(plevel)+' hPa')

ax2 = fig.add_subplot(gs[0,1])
dir = "D://thesisdata/bilder/wetter3de/10mwind/"
zeitstr = str(zeitpunkt)
pic = (zeitstr[:4]+zeitstr[5:7]+zeitstr[8:10]
        +zeitstr[11:13]+'_7_au.gif')
pic
img=mpimg.imread(dir+pic)

imgplot = ax2.imshow(img[200:472,200:570])
ax2.axis('off')
ax2.set_title('10m Wind über Grund [kn] - GFS - wetter3.de')

ax3 = fig.add_subplot(gs[0,2])

imgplot2 = ax3.imshow(img[10:470,640:680])
ax3.axis('off')

fig.savefig(
     'D://thesisdata/bilder/combinations/wind/'
     +zeitstr[:13]+'.png', dpi = 500
     )
#plt.show()
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
