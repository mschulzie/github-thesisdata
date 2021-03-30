import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature

stations = pd.read_csv('./Python/air_quality/clean.csv',parse_dates=True,
    index_col='time')
timestamp = '2009-09-23T00'
var = 'PM10'
stations = stations[timestamp]
stations = stations[stations.variable==var]

fig = plt.figure()
ax = fig.add_subplot(111, projection=crs.PlateCarree())
ax.coastlines(lw=.5, zorder=5)
ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=1)
ax.add_feature(cfeature.STATES,lw=.2, zorder=2)
ax.scatter(stations.lon,stations.lat,s=50,zorder=3,color='purple')
ax.set_title(str(stations.station.size)+ ' stations with '+var+ ' variable \n'+
    'at '+timestamp)
