import wrf
import xarray as xr
import netCDF4
import numpy as np
import warfy as wh
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

#file = '/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00'
file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'
constvar = ['VEGFRA','IVGTYP','ISLTYP','ROUGH_COR',
    'LAI','HGT']
timevar = ['uvmet','SMOIS_COR','UST','UST_T']
# only  SMOIS_COR, UST and UST_T variable in time!!
test = wh.Warfy()
test.load_var(file,constvar)
test.load_var(file,timevar)

emis = ['DUST_EMIS_ACC1','DUST_EMIS_ACC2','DUST_EMIS_ACC3','DUST_EMIS_ACC4','DUST_EMIS_ACC5']
test.load_var(file,emis)
test.sum_vars(emis,'DUST_EMIS_ACC_SUM')
#%%
#TEST
lo = 62
la = 92
test.get_var('UST').isel(lon=lo,lat=la).plot(label='UST')
test.get_var('UST_T').isel(lon=lo,lat=la).plot(label='UST_T')
(test.get_var('DUST_EMIS_ACC_SUM')/100).isel(lon=lo,lat=la).plot(label='DUST_EMIS_ACC_SUM / 100')
#test.get_var('uvmet_speed').isel(lon=lo,lat=la).plot(label='wind')
plt.legend()
plt.savefig('gridcell_no_emission.png')
#%%

test = test.isel(lon=slice(50,70),lat=slice(80,100))
test.windspeed(unit='km/h')
#%%
highest_lon=[140.02089,140.50768,140.50768,140.99446,140.02089,140.02089,
    140.02089,140.99446,140.99446,139.04732,136.61339,138.07375,140.50768,
    129.3116,138.56053,142.45482,140.99446,138.07375,142.45482,141.48125]
highest_lat = ([-25.154457,-23.379456,-23.825523,-23.379456,
    -23.825523,-24.27005,-23.379456,-23.825523,
    -24.713036,-23.825523,-28.198704,-27.768837,
    -24.713036,-31.574299,-27.337261,-24.713036,
    -24.27005,-27.337261,-24.27005,-23.379456])

#%%
area = [135,144,-21,-28]
wind = test.get_var('uvmet_speed')
wind.name
widths = [5,5]
heights = [1,1,1,2,2,2]
fig = plt.figure(figsize=(10,20))
gs = fig.add_gridspec(6, 2,width_ratios=widths,
    height_ratios=heights,wspace=0.05,hspace=0.1)
ax0 = fig.add_subplot(gs[0,:])
test.get_var('DUST_EMIS_ACC_SUM').mean(dim=('lat','lon')).plot(ax=ax0,
    label='dust emission in '+
    test.get_var('DUST_EMIS_ACC_SUM').units+' (maxval=121!!)',
    color='purple')
ax0.legend(fontsize=8)
ax0.grid()
ax0.set_xticklabels('')
ax0.set_xlabel('')
ax0.set_title('mean values for selected area')

ax = fig.add_subplot(gs[1,:])
wind.mean(dim=('lat','lon')).plot(ax=ax,label='Wind in '+
    wind.units+' at groundlevel')
ax.legend(fontsize=8)
ax.grid()
ax.set_xticklabels('')
ax.set_xlabel('')

ax2 = fig.add_subplot(gs[2,:])
for t in timevar[1:]:
    test.get_var(t).mean(dim=('lat','lon')).plot(ax=ax2,label=t+' in '+
        test.get_var(t).units)
ax2.legend(fontsize=8)
ax2.grid()
ax2.set_xlabel('')
ax2.set_xticklabels(['19. Sep','21. Sep','23. Sep',
    '25.Sep','27.Sep','29. Sep'],rotation=0)
wind.coords
wind.attrs
# ax.set_ylabel('')

# ax.set_yticks(np.arange(0,limit+step,step))
# ax.set_xticklabels(['19.09.','21.09.','23.09.','25.09.','27.09.',
#     '29.09.'])

cmaps = ['Greens','tab20','tab20','jet','Greens','Blues']

# number of different values..:
list(set(test.get_var('ISLTYP').values[0,...].flatten().tolist()))

i=0
row=3
for c in constvar:
    map = fig.add_subplot(gs[row,i], projection=crs.Mercator(central_longitude=150.0))
    levels = list(set(test.get_var('IVGTYP').values[0,...].flatten().tolist()))
    im = map.pcolormesh(test.get_var(c).lon.values,test.get_var(c).lat.values,
        test.get_var(c).max('time').values, transform=crs.PlateCarree(),
        zorder=1,cmap=cmaps.pop(0))
    map.add_feature(cfeature.STATES,lw=.5, zorder=2,edgecolor='black')
    map.set_title(c+': '+test.get_var(c).attrs['description'] +
        ' in ' + test.get_var(c).attrs['units'])
    gl = map.gridlines(
        crs=crs.PlateCarree(),
        draw_labels=True,
        linewidth=1, color='grey', linestyle='dotted',
        zorder=6)
    cb = plt.colorbar(im,shrink=0.7,aspect=40)
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False
    gl.xlocator = mticker.FixedLocator([area[0]+0.1,area[1]-0.1])
    gl.ylocator = mticker.FixedLocator([area[2]-0.1,area[3]+0.1])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    for k in range(len(highest_lon)):
        if ((area[0]<highest_lon[k]<area[1])&
            (area[3]<highest_lat[k]<area[2])):
            map.text(highest_lon[k],highest_lat[k],str(k+1),transform=
                crs.PlateCarree(), ha='center',va='center',zorder=3,
                fontsize=8)
    map.set_extent(area,crs=crs.PlateCarree())

    i += 1
    if i == 2:
        gl.right_labels = True
        row += 1
        i = 0


# fig.suptitle('Times series of first '+str(N)+
#     ' max values (DUST_EMIS_ACC_1-5) \n'+ 'and locations on map')
# plt.tight_layout()
#plt.tight_layout()
plt.show()

fig.savefig('D://thesisdata/emission_controls.pdf')
