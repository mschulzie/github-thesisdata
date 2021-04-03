import wrf
import xarray as xr
import netCDF4
import numpy as np
import wrfhelper_neu as wh
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

file = '/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00'
#file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'
var = ['DUST_EMIS_ACC1','DUST_EMIS_ACC2','DUST_EMIS_ACC3','DUST_EMIS_ACC4','DUST_EMIS_ACC5']

test = wh.Warfy()
test.load_var(file,var)
test.sum_vars(var,'DUST_EMIS_ACC_SUM')
test.load_var(file,'uvmet10')
test.load_var(file,'ROUGH_COR')
rough = test.get_var('ROUGH_COR')
wind = test.get_var('uvmet10')
varr = test.get_var('DUST_EMIS_ACC_SUM')
maxvals = varr.max('time')
maxvals.argmax(dim=('lon','lat'))['lon']
wind = np.sqrt(wind[0,...]**2 +wind[1,...]**2)*3.6
rough = 10 * rough

# N highest values:
N = 20
widths = [5,5]
fig = plt.figure(figsize=(5,2*N),constrained_layout=True)
gs = fig.add_gridspec(N, 2,width_ratios=widths,wspace=0.05)

for i in range(N):
    ax = fig.add_subplot(gs[i,0])
    map = fig.add_subplot(gs[i,1], projection=crs.Mercator(central_longitude=150.0))
    ilon = maxvals.argmax(dim=('lon','lat'))['lon'].values
    ilat = maxvals.argmax(dim=('lon','lat'))['lat'].values
    lon = maxvals[maxvals.argmax(dim=('lon','lat'))].lon.values
    lat = maxvals[maxvals.argmax(dim=('lon','lat'))].lat.values
    wind[maxvals.argmax(dim=('lon','lat'))].plot(ax=ax,
        label='10m wind in km/h', color='red')
    varr[maxvals.argmax(dim=('lon','lat'))].plot(ax=ax,
        label='DUST_EMIS_ACC_1-5 in ug/m2/s', color='black')
    rough[maxvals.argmax(dim=('lon','lat'))].plot(ax=ax,
        label='10 x roughness elements corr.', color='green')
    limit = varr[maxvals.argmax(dim=('lon','lat'))].max()
    if (wind[maxvals.argmax(dim=('lon','lat'))].max() >
        varr[maxvals.argmax(dim=('lon','lat'))].max()):
        limit = wind[maxvals.argmax(dim=('lon','lat'))].max()
    step = limit // 7
    ax.legend(fontsize=4)
    maxvals[maxvals.argmax(dim=('lon','lat'))] = 0
    ax.set_title('Indexes: idxlon='+str(ilon)+', idxlat='+str(ilat),fontsize=8)
    ax.grid()
    map.coastlines(lw=.5, zorder=2)
    map.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    map.add_feature(cfeature.LAND, fc='white', zorder=1)
    map.add_feature(cfeature.STATES,lw=.2, zorder=2)
    map.add_feature(cfeature.OCEAN,fc='lightblue')
    gl = map.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=1, color='red', linestyle='dotted',
        zorder=6)
    gl.top_labels = False
    gl.left_labels = False
    gl.xlocator = mticker.FixedLocator([lon])
    gl.ylocator = mticker.FixedLocator([lat])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    map.plot(lon,lat,'x',color='red',markersize=10,transform=crs.PlateCarree())
    map.set_extent([112,155,-10,-40],crs=crs.PlateCarree())
    ax.set_ylabel('')
    ax.set_xticklabels('')
    ax.set_xlabel('')
    ax.set_yticks(np.arange(0,limit+step,step))

ax.set_xticklabels(['19.09.','21.09.','23.09.','25.09.','27.09.',
        '29.09.'])
fig.suptitle('Times series of first '+str(N)+
    ' max values (DUST_EMIS_ACC_1-5) \n'+ 'and locations on map')
plt.tight_layout()
plt.show()

fig.savefig('high_emissions_20.pdf')
