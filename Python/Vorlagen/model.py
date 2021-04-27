from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import warfy
from netCDF4 import Dataset
import wrf

r_pol = 12713.504/2
r_eq = 12756.320/2
#%%
file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'

fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot(111,projection='3d')
x_scale=5
y_scale=5
z_scale=1

scale=np.diag([x_scale, y_scale, z_scale, 1.0])
scale=scale*(1.0/scale.max())
scale[3,3]=1.0

def short_proj():
  return np.dot(Axes3D.get_proj(ax), scale)

ax.get_proj=short_proj

height = wrf.getvar(Dataset(file),'z')
hgt = wrf.getvar(Dataset(file),'HGT').values
land = wrf.getvar(Dataset(file),'LANDMASK').values == 1
land.shape
hgt.shape
hgt[land==False] = np.nan
height.coords

x = height.west_east.values
y = height.south_north.values
z = height.bottom_top.values
height= height.values
ax.set_xticks(x)
ax.set_yticks(y)
ax.set_zticks(z)
ax.set_zlim(0,32)
fontsize= 30
ax.set_xticklabels(['0']+[None]*162+['163'],fontsize=fontsize)
ax.set_yticklabels(['0']+[None]*122+['123'],fontsize=fontsize)
ax.set_zticklabels(['0']+[None]*30+['31'],fontsize=fontsize)
X,Y = np.meshgrid(x,y)
im = ax.contourf(X,Y,hgt,offset=1,cmap='terrain')
cb = plt.colorbar(im,shrink=0.8)
cb.set_label('Höhe des Gitterpunkts im Modell in m',fontsize=fontsize)
cb.ax.tick_params(labelsize=fontsize)
[None]*10
#plt.pcolormesh(X,Y,hgt,cmap='plasma')
plt.grid()
plt.savefig('model.png',dpi=300)
plt.show()
# lon = height.XLONG.values[0,:]
# lat = height.XLAT.values[:,0]
# np.diff(lon)
# np.diff(lat)
# 2*np.pi*r_pol*np.diff(lat).min()/360
# 2*np.pi*r_pol*np.diff(lat).max()/360
# 2*np.pi*r_eq*np.diff(lon)[0]/360 * np.cos(lat.max()/360*2*np.pi)
# 2*np.pi*r_eq*np.diff(lon)[0]/360 * np.cos(lat.min()/360*2*np.pi)
