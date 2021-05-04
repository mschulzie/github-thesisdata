import wrf
import xarray as xr
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import copy as cp

# from matplotlib.cm import get_cmap
# from matplotlib.colors import LogNorm
# import matplotlib.ticker as mticker
# import cartopy.crs as crs
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import numpy as np
# import cartopy.feature as cfeature
# import os
#file = '/home/julchen/Studium/wrfout_d01_2009-09-18_00_00_00'
file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'

#%%
class Warfy:
    def __init__(self, file=None, var=None):
        self._vars = {}

        if (file is not None) and (var is not None):
            self.load_var(file, var)

        self.vars = self._vars.keys()
        self.check_dims()

    def load_var(self, vars, file=file, slevel=0, zlevel=0):
        dataset = netCDF4.Dataset(file)
        if (type(vars)==str):
            vars = [vars]
        for var_name in vars:
            ds = wrf.getvar(dataset,var_name,timeidx=wrf.ALL_TIMES)
            lons = ds.XLONG.isel(south_north=0).values
            dims = ['time','lat','lon']
            coords = {
                'time'  : ds.Time.values,
                'lat'   : ds.XLAT.isel(west_east=0).values,
                'lon'   : np.mod(lons, 360)
                }
            attrs = ds.attrs
            # select a zlevel
            try:
                ds = ds.sel(bottom_top=zlevel)
                attrs['description'] += ' at zlevel {:}'.format(zlevel)
            except ValueError:
                pass
            try:
                ds = ds.sel(soil_layers_stag=slevel)
                attrs['description'] += ' at slevel {:}'.format(slevel)
            except ValueError:
                pass
            # add u_v coordinate for wind fields
            try:
                ds.coords['u_v']
                uv = ['u','v']
                dims.insert(0,'u_v')
                coords['u_v'] = uv
            except KeyError:
                pass

            new_ds = xr.DataArray(
                ds.values,
                dims = dims,
                coords = coords,
                attrs = attrs
                )

            self._vars[var_name] = new_ds
        self.check_dims()

    def check_dims(self):
        for v in self._vars:
            size = self._vars[v].time.size
            start = self._vars[v].time[0]
            stop = self._vars[v].time[-1]
        for v in self._vars:
            if (size != self._vars[v].time.size):
                raise UserWarning('DataArrays have different number of timesteps')
            if (start != self._vars[v].time[0]):
                raise UserWarning('DataArrays have different starting points(time)')
            if (stop != self._vars[v].time[-1] ):
                raise UserWarning('DataArrays have different end points(time)')
            self.time = self._vars[v].time

    def get_var(self, var=None):
        try:
            return self._vars[var]
        except KeyError:
            return self._vars

    def remove_var(self, *vars):
        for v in vars:
            self._vars.pop(v)

    def sum_vars(self, vars, new, drop=True, keep_attrs=True,
        description=None):
        temp = self.get_var(vars[0]).fillna(0)
        attrs = self.get_var(vars[0]).attrs
        for v in vars[1:]:
            temp += self.get_var(v).fillna(0)

        if keep_attrs:
            temp.attrs = attrs

        if (description != None):
            temp.attrs['description'] = description

        self._vars[new] = temp

        if drop:
            self.remove_var(*vars)

    def windspeed(self,drop=True,unit='kt'):
        units = {'km/h': 3.6, 'm/s':1,'kt':1.94384}
        new_vars = {}
        for v in self._vars:
            if ('u_v' in self._vars[v].dims):
                attrs = self._vars[v].attrs
                coords = {
                    'time'  : self._vars[v].time.values,
                    'lat'   : self._vars[v].lat.values,
                    'lon'   : self._vars[v].lon.values
                    }
                new_ds = xr.DataArray(
                    (np.sqrt(self._vars[v].values[0,...]**2+
                        self._vars[v].values[1,...]**2)
                        * units[unit]) ,
                    dims = ['time','lat','lon'],
                    coords = coords,
                    attrs = attrs
                    )
                new_ds.attrs['units'] = unit
                new_vars[v+'_speed'] = new_ds
        self._vars.update(new_vars)
        if drop:
            for v in list(self._vars):
                if ('u_v' in self._vars[v].dims):
                    self._vars.pop(v)

    def sel(self,**kwargs):
        temp = Warfy()
        for v in self._vars:
            temp._vars[v] = self._vars[v].sel(kwargs)
        temp.check_dims()
        return temp

    def isel(self,**kwargs):
        temp = Warfy()
        for v in self._vars:
            temp._vars[v] = self._vars[v].isel(kwargs)
        temp.check_dims()
        return temp

    def plot(self,**kwargs):
        timesteps = self.time.size
        if (timesteps > 10):
            raise RuntimeError('Too many timesteps ('+str(timesteps)+
            '). First slice! Limit is 10. Else I wont'+
            ' be able to plot that huge figure')
        vars = len(self._vars)
        fig = plt.figure(figsize=(5*timesteps,3.2*vars))
        gs = fig.add_gridspec(vars,timesteps,hspace=0.4)
        count_var = 0
        for v in self._vars:
            for i in range(timesteps):
                ax = fig.add_subplot(gs[count_var,i])
                self._vars[v].isel(time=i).plot(ax=ax,**kwargs)
            count_var += 1
        plt.show()
        return fig
