from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature
import wrf
import xarray as xr
ncfile = Dataset("D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00")
varname = "DUSTLOAD_ACC_"
binmax = 5
vars = [None]*binmax

for binsize in range(binmax):
    vars[binsize] = wrf.getvar(ncfile,varname+str(binsize+1),timeidx=wrf.ALL_TIMES)
    vars[binsize] = vars[binsize].isel(west_east=slice(0,143))

lats, lons = wrf.latlon_coords(vars[0])
cart_proj = wrf.get_cartopy(vars[0])

var = vars[0]+vars[1]+vars[2]+vars[3]+vars[4]
#var = var.where(var>1000)
levels = np.linspace(1000,1e6,101).tolist()

#%%

zeitpunkt = '2009-09-24T00'

for zeitpunkt in var.coords['Time'].values: # dann plt.show() rausnehmen

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
                     cmap=get_cmap('plasma'),alpha=1,levels=levels,extend='max')
    cb=plt.colorbar(ax=ax, shrink=.98,
                        label=('Sum of '+vars[0].description[:-2]+'s 1-5 in '
                        +vars[0].units))
    #cb.set_ticks(cblevels)
    ax.set_xlim(wrf.cartopy_xlim(vars[0]))
    ax.set_ylim(wrf.cartopy_ylim(vars[0]))
    # Add the gridlines
    #ax.gridlines(color="black", linestyle="dotted")
    gl = ax.gridlines(
        crs=crs.PlateCarree(), draw_labels=True,
        linewidth=1, color='gray', linestyle='dotted',
        xlocs=[120,135,150,165,180], zorder=6
        )
    gl.top_labels = False
    gl.right_labels = False

    vars[0].description[:-1]

    plt.title(str(zeitpunkt)[:13]+' - DUSTLOAD_ACC_')

    fig.savefig(
                'D://thesisdata/bilder/Python/wrfout/'+varname+'/'
                +str(zeitpunkt)[:13]+'.png', dpi = 300
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
