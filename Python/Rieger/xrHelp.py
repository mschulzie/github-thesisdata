#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nrieger
@email: niclasrieger@gmail.com

@description: Compilation of helper functions for time series anaylsis
"""

import numpy as np
import xarray as xr

def remove_seasonal_cycle(array, time_format):
    """ Remove seasonal cycle by removing mean values.

    Parameters
    ----------
    array : DataArray
        Data to remove seasonal cycle from
    time_format : str
        Temporal resolution, e.g. 'time.month'.

    Returns
    -------
    DataArray
        Data without seasonal cycle.
    """
    return array.groupby(time_format) - array.groupby(time_format).mean()

def moving_average(array, window):
    if window > 1:
        if (window % 2) == 1:
            averaged = array.rolling({'time' : window}, center=True).mean()

            cut = window // 2
            return averaged[cut:-cut,:,:]
        else:
            raise ValueError("Window needs to be odd.")
    return array


def select_months(data,*months):
    """Select specific months from a xarray DataArray.

    Parameters
    ----------
    data : xr.DataArray
        .
    *months : (list of) int
        Months are decoded by int, i.e. 1=Jan, ..., 12=Dec.

    Returns
    -------
    xr.DataArray
        DataArray which contains only the specified months.

    """

    subData = []
    for mon in months:
        mask = (data['time.month'] == mon)
        subData.append(data[mask])

    mergedData = xr.merge(subData)
    variable = list(mergedData.data_vars.keys())[0]
    return mergedData[variable]


def wrap_lon_180to360(ds, lon='lon'):
    """
    wrap longitude coordinates to 0..360

    Parameters
    ----------
    ds : Dataset
        object with longitude coordinates
    lon : string
        name of the longitude ('lon', 'longitude', ...)

    Returns
    -------
    wrapped : Dataset
        Another dataset array wrapped around.
    """

    # wrap -180..179 to 0..359
    ds = ds.assign_coords(lon=np.mod(ds[lon], 360))

    # sort the data
    return ds.sortby(lon)


def wrap_lon_360to180(ds, lon='lon'):
    """
    wrap longitude coordinates to 0..360

    Parameters
    ----------
    ds : Dataset
        object with longitude coordinates
    lon : string
        name of the longitude ('lon', 'longitude', ...)

    Returns
    -------
    wrapped : Dataset
        Another dataset array wrapped around.
    """

    # wrap 0..359 to -180..179
    ds = ds.assign_coords(lon=(((ds[lon] + 180) % 360) - 180))

    # sort the data
    return ds.sortby(lon)
