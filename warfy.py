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

    def load_var(self, file, vars, slevel=0, zlevel=0):
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

    def plot(self):
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
                self._vars[v].isel(time=i).plot(ax=ax)
            count_var += 1
        plt.show()


#%%

def wrfplot(wrffile,varname,compare_var=None,time='2009-09-18T00',ppfig=(1,1),
    save=False,savedir=None,show=True,cmap='RdBu_r', qmin=0,
    qmax=1, levels=50,limmin=None,limmax=None,zlevel=None,plevel=None,
    contour_color='black', contour_levels=10, cities=None,
    lons = (110.3,-170),lats = (-57.06,-9.5),
    only_maxvals=False):
    """
    Just a wrapper to easily plot wrfout with given latitude and
    longitude limits (Australia+Southern Ocean) for the purpose of
    consistent plots of different variables.
    """
    #ADD: second variable (optionally) to compare (contour)

    #ADD: interpolation at specific heightevel for 4D variables.

    var, cvar, vector, u, v = loadvar(
        wrffile,varname,units="kt",plevel=plevel,zlevel=zlevel,
        lons=lons,lats=lats)

    if (compare_var!=None):
        var2, cvar2, vector2, u2, v2 = loadvar(wrffile,compare_var,
            units="kt",plevel=plevel,zlevel=zlevel,lons=lons,lats=lats)
        var2 = var2.sel(Time=time)
        cvar2 = cvar2.sel(Time=time)
        if vector:
            u2 = u2.sel(Time=time)
            v2 = v2.sel(Time=time)

    lats, lons = wrf.latlon_coords(var)
    lons = np.mod(lons,360)
    cart_proj = wrf.get_cartopy(var)
    cb_fontsize = 8
    #Computes the limits from which data should be shown by using quantiles

    if (type(levels) == int):
        if (limmin==None):
            limmin = cvar.quantile(qmin)
        if (limmax==None):
            if (cvar.quantile(qmax)>10):
                limmax = (int(np.round(cvar.quantile(qmax),
                    -len(str(int(cvar.quantile(qmax))))+4)))
            else:
                limmax = (np.round(cvar.quantile(qmax),3))

        c_levels = np.linspace(limmin,limmax,levels)

        #Computes ticks for colorbar
        if (limmin>1):
            cbar_min = int(np.round(limmin,-len(str(int(limmax)))+4))
        else:
            cbar_min = np.round(limmin,3)
        cbar_max = limmax
        if ((cbar_max-cbar_min) > 10):
            cbar_step = int((cbar_max-cbar_min)/10)
        else:
            cbar_step = (cbar_max-cbar_min)/10
        cbarticks = np.arange(cbar_min, cbar_max+cbar_step,cbar_step)
        if (len(cbarticks)>levels):
            cbarticks = c_levels
        if (limmax < 10):
            cbformat = '%.3f'
        elif (limmax < 99999):
            cbformat = '%d'
        else:
            cbformat = '%.1E'
        levelnorm = None
    if (type(levels) == list):
        cbformat = '%.1E'
        c_levels = levels
        cbarticks = levels
        levelnorm = LogNorm()


    var = var.sel(Time=time)
    cvar = cvar.sel(Time=time)
    if vector:
        u = u.sel(Time=time)
        v = v.sel(Time=time)
    t=0
    while (t<var.Time.size):
    #for t in range(var.Time.size//(ppfig[0]*ppfig[1]+1)+1):
        fig = plt.figure(figsize=(5*ppfig[1],3.2*ppfig[0]))
        gs = fig.add_gridspec(ppfig[0],ppfig[1],hspace=0.4)
        count = 0
        for i in range(ppfig[0]):
            for j in range(ppfig[1]):
                ax = fig.add_subplot(gs[i,j], projection=cart_proj)
                ax.coastlines(lw=.5, zorder=5)
                ax.add_feature(cfeature.BORDERS, lw=.5, zorder=5)
                ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
                ax.add_feature(cfeature.STATES,lw=.2, zorder=5)
                if only_maxvals:
                    cvar_t = cvar.max(dim='Time')
                elif (var.Time.size > 1):
                    cvar_t = cvar.isel(Time=t+count)
                else:
                    cvar_t = cvar
                cvar_contour = ax.contourf(wrf.to_np(lons), wrf.to_np(lats),
                    wrf.to_np(cvar_t),
                    zorder=4, transform=crs.PlateCarree(),
                    cmap=cmap,alpha=1,levels=c_levels,extend='max',
                    norm = levelnorm)
                cb = plt.colorbar(cvar_contour, shrink=.98,
                    format=cbformat)
                cb.set_ticks(cbarticks)
                cb.ax.tick_params(labelsize=cb_fontsize)
                cblabel = var.description+' in '+var.units
                if (len(cblabel) > 40):
                    c = 0
                    for letter in cblabel[40:]:
                        if (letter == ' '):
                            cblabel = cblabel[:40+c]+'\n'+cblabel[40+c:]
                            break
                        c += 1
                cb.set_label(label=(cblabel),
                    fontsize=cb_fontsize)

                if vector:
                    each = 8
                    if (var.Time.size > 1):
                        u_t = u.isel(Time=t+count)
                        v_t = v.isel(Time=t+count)
                    else:
                        u_t = u
                        v_t = v
                    plt.barbs(wrf.to_np(lons[::each,::each]),
                        wrf.to_np(lats[::each,::each]),
                        wrf.to_np(u_t[::each,::each]),
                        wrf.to_np(v_t[::each,::each]),
                        zorder=7, transform=crs.PlateCarree(), color="grey",
                        length=4)
                if only_maxvals:
                    zeitstr = str(time.start)[5:10]+' - '+str(time.stop)[5:10]
                    t = var.Time.size - 1
                else:
                    zeitstr = str(cvar_t.Time.values)
                title = zeitstr[:13]+' (WRF)'+' - '+ varname
                if (compare_var!=None):
                    if (var.Time.size > 1):
                        cvar2_t = cvar2.isel(Time=t+count)
                    else:
                        cvar2_t = cvar2
                    compvar_contour = ax.contour(
                        wrf.to_np(lons), wrf.to_np(lats),
                        wrf.to_np(cvar2_t),
                        zorder=6, transform=crs.PlateCarree(),
                        colors=contour_color,
                        linewidths=.5,linestyles='solid',
                        levels=contour_levels)
                    #Update matplotlib to latest version!! else no clabel zorder
                    clabels = compvar_contour.clabel(zorder=7, inline=True,
                        fontsize=4,fmt='%d',inline_spacing=0)
                    ax.text(lons[0,-2],lats[1,0],'Contours: '+
                        str(var2.description)+
                        ' in '+str(var2.units),
                        fontsize=4,zorder=8,transform=crs.PlateCarree(),
                        ha='right',
                        bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 1})
                    title=title+'-'+compare_var
                ax.set_xlim(wrf.cartopy_xlim(var))
                ax.set_ylim(wrf.cartopy_ylim(var))
                gl = ax.gridlines(
                    crs=crs.PlateCarree(),
                    draw_labels=True,
                    linewidth=1, color='gray', linestyle='dotted',
                    zorder=6)
                gl.top_labels = False
                gl.right_labels = False
                gl.xlocator = mticker.FixedLocator([120,135,150,165,180])
                gl.ylocator = mticker.FixedLocator([-10,-20,-30,-40,-50])
                gl.xformatter = LONGITUDE_FORMATTER
                gl.yformatter = LATITUDE_FORMATTER
                if cities!=None:
                    transa = crs.PlateCarree()._as_mpl_transform(ax)
                    for city in cities:
                        ax.text(cities[city][0]+.1,cities[city][1]+.1,
                            city,fontsize=2,
                            zorder=8,transform=crs.PlateCarree(),ha='left')
                        ax.plot(cities[city][0],cities[city][1],color='red',
                            zorder=7,transform=crs.PlateCarree(),
                            marker='o',markersize=.2)
                if only_maxvals:
                    ax.set_title(title+ '\n maximum values each grid point',
                        fontsize=10)
                else:
                    ax.set_title(title,fontsize=10)
                count += 1
                if (t+count==var.Time.size):
                    break
            else:
                continue
            break
        if save:
            multi =''
            if (savedir==None):
                print('Give path to save figures!!')
            if (ppfig[0]*ppfig[1] > 1):
                multi = '_multi_'+str(ppfig[0])+'x'+str(ppfig[1])
            if (title[22:] not in os.listdir(savedir+'Python/wrfout/')):
                os.mkdir(savedir+'Python/wrfout/'+title[22:])
            fig.savefig(savedir+'Python/wrfout/'+title[22:]+'/'+title[:13]
                +multi+'.png', dpi = 500)
        if show:
            plt.show()
        plt.close()
        t += ppfig[0]*ppfig[1]
    return var
