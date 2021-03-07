from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import numpy as np
import xarray as xr

from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, extract_vars)

# Extract names of variables
# ds = xr.open_dataset("D://thesisdata/wrfout_d01_2009-09-18_00_00_00")
# f = open('varnames_wrfout.txt','w+')
# f.write('Insgesamt ' + str(len(ds.data_vars)) + ' Variablen: \n')
# for line in ds.data_vars:
#     if (line == "Times"):
#         f.write(str(ds.data_vars[str(line)].name) + '\n')
#     else:
#         f.write(
#                 str(ds.data_vars[str(line)].name)+';'+
#                 str(ds.data_vars[str(line)].attrs['description']) + ';' +
#                 str(ds.data_vars[str(line)].values.max())+
#                 '\n'
#                 )
# f.close()

ncfile = Dataset("D://thesisdata/wrfout_d01_2009-09-18_00_00_00")
# Get the sea level pressure
slp = getvar(ncfile, "DUST_1")
slp.coords
slp.shape
slp.dims
slp.max()

# Smooth the sea level pressure since it tends to be noisy near the
# mountains
# Get the latitude and longitude points
lats, lons = latlon_coords(slp)
# Get the cartopy mapping object
cart_proj = get_cartopy(slp)

# Create a figure
fig = plt.figure(figsize=(12,6))
# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
                             facecolor="none",
                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)

# Make the contour outlines and filled contours for the smoothed sea level
# pressure.
plt.contour(to_np(lons), to_np(lats), to_np(slp), colors="black",
            transform=crs.PlateCarree(central_longitude=180.0))
plt.contourf(to_np(lons), to_np(lats), to_np(slp),
             transform=crs.PlateCarree(central_longitude=180.0),
             cmap=get_cmap("viridis"))

# Add a color bar
plt.colorbar(ax=ax, shrink=.98, )

# Set the map bounds
ax.set_xlim(cartopy_xlim(slp))
ax.set_ylim(cartopy_ylim(slp))

# Add the gridlines
ax.gridlines(color="black", linestyle="dotted")

plt.show()
