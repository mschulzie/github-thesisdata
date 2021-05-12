from warfy import Warfy
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import helperlies as mway
from mpl_toolkits.mplot3d import Axes3D

varname = 'DUST_SOILFE_ACC'
var = [varname] * 5
var = [var[i]+'_'+str(i+1) for i in range(5)]

test = Warfy()
test.load_var(var)
test.sum_vars(var,varname)
test.load_var('QCLOUD')
test.load_var('HGT')
hgt = test.get_var('HGT').isel(time=0).values
dust = test.get_var(varname).sel(time='2009-09-22T15')
cloud = test.get_var('QCLOUD').sel(time='2009-09-22T15')
dust.values[dust.values<1e-4]= np.nan
cloud.values[cloud.values==0] = np.nan
#%%
fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot(111,projection='3d')
# Scaling output ----
x_scale=5
y_scale=5
z_scale=5

scale=np.diag([x_scale, y_scale, z_scale, 1.0])
scale=scale*(1.0/scale.max())
scale[3,3]=1.0

def short_proj():
  return np.dot(Axes3D.get_proj(ax), scale)
ax.get_proj=short_proj
#-----
z = dust.zlevel.values
ax.set_zticks(z)
ax.set_zlim(0,32)
LAT, LON = np.meshgrid(dust.lat.values,dust.lon.values)
# set landmask:
test.load_var('LANDMASK')
land = (test.get_var('LANDMASK').isel(time=0).values == 1)
hgt[land==False]=np.nan
ax.contourf(LON,LAT,hgt.transpose(),cmap='gray',offset=0,
    levels=50)
# ---

for i in range(32):
    if np.isnan(dust.sel(zlevel=i).values).all():
        print('dust zlevel {:} empty!'.format(i))
    else:
        ax.contour(LON,LAT,dust.sel(zlevel=i).values.transpose(),
            offset=i,cmap='Reds',alpha=.8)
for i in range(32):
   if np.isnan(cloud.sel(zlevel=i).values).all():
       print('cloud zlevel {:} empty!'.format(i))
   else:
       ax.contour(LON,LAT,cloud.sel(zlevel=i).values.transpose(),
           cmap='Blues',alpha=.8,offset=i)
ax.view_init(elev=20, azim=235)
#fig.savefig('D://thesisdata/bilder/3D/test.png',dpi=500)
plt.show()
