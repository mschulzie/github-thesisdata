import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as crs
import cartopy.feature as cfeature
import os
import numpy as np

of_raw = pd.read_csv('./Python/air_quality/official_data.csv',
    parse_dates=True, index_col='time')
dw_raw = pd.read_csv('./Python/air_quality/dustwatch_data.csv',
    parse_dates=True, index_col='time')
timestamp = '2009-09-23T00'
var = 'PM10'


daterange = pd.date_range(timestamp,timestamp,freq='1H')

for timestamp in daterange:
    timestr = str(timestamp)[:13]
    of = of_raw[timestr]
    dw = dw_raw[timestr]
    of = of[of.variable==var]
    of.fillna(0,inplace=True)
    of = of.sort_values('value',ascending=True,na_position='first')
    dw = dw.sort_values('value',ascending=True,na_position='first')

    official_label = str(of.station.size)+ ' regular stations'
    dustwatch_label = str(dw.station.size)+ ' DustWatch stations'

    color_levels = {'white'  :(0,dustwatch_label,official_label),
                    'lightblue':(1,None,None),
                    'blue'   :(25,None,None),
                    'lime'  :(100,None,None),
                    'green'  :(1000,None,None),
                    'yellow' :(2000,None,None),
                    'orange' :(5000,None,None),
                    'red'    :(10000,None,None),
                    'magenta':(15387,None,None)}

    cmap = mpl.colors.ListedColormap(list(color_levels))
    bounds = np.arange(len(color_levels)+1).tolist()

    fig = plt.figure(figsize=(8,8))
    widths = [10,1]
    gs = fig.add_gridspec(1, 2,width_ratios=widths,wspace=0.05)
    ax = fig.add_subplot(gs[0,0], projection=crs.PlateCarree())
    cb = fig.add_subplot(gs[0,1])
    ax.coastlines(lw=.5, zorder=2)
    ax.add_feature(cfeature.BORDERS, lw=.5, zorder=2)
    ax.add_feature(cfeature.LAND, fc='white', zorder=1)
    ax.add_feature(cfeature.STATES,lw=.2, zorder=2)

    for level in color_levels:
        dw_lvl = dw[dw.value>=color_levels[level][0]]
        of_lvl = of[of.value>=color_levels[level][0]]
        im2 = ax.scatter(dw_lvl.lon,dw_lvl.lat,s=60,zorder=3,
            color=level,marker='s',alpha=1,label=color_levels[level][1],
            edgecolors='black')
        im1 = ax.scatter(of_lvl.lon,of_lvl.lat,s=50,zorder=3,
            color=level,label=color_levels[level][2],
            marker='X',edgecolors='black')

    # plt.colorbar(im1,label='Regular PM10 concentrations in ug/m3',
    #     orientation='horizontal',shrink=.2)
    # plt.colorbar(im2,label='DustWatch (???) PM10 concentrations in ug/m3',
    #     orientation='horizontal',shrink=.2)

    for stat in of.station:
        ax.text(of[of.station==stat].lon.values+.2,
            of[of.station==stat].lat.values+.2,
            stat,fontsize=4,
            zorder=4,transform=crs.PlateCarree(),ha='left')
    for stat in dw.station:
        ax.text(dw[dw.station==stat].lon.values+.2,
            dw[dw.station==stat].lat.values+.2,
            stat,fontsize=4,
            zorder=4,transform=crs.PlateCarree(),ha='left')
    coba = mpl.colorbar.ColorbarBase(ax=cb,cmap=cmap,orientation='vertical',
        spacing='uniform',boundaries=bounds,
        label =r'measured concentrations in $\mu$g / m$^3$')
    labels = [None]*len(color_levels)
    i = 0
    for step in color_levels:
        if color_levels[step][0] > 99999:
            labels[i] = '{:.0e}'.format(int(color_levels[step][0]))
        else:
            labels[i] = '{:d}'.format(int(color_levels[step][0]))
        i+=1
    coba.set_ticklabels(labels)
    title=(timestr)
    ax.set_title(title)
    ax.legend()

    # fig.savefig('D://thesisdata/bilder/Python/dustwatch/'+
    #      timestr+'.png',dpi=300)
    # plt.close()
