import wrf
import xarray as xr
import netCDF4
import numpy as np


# import matplotlib.pyplot as plt
# from matplotlib.cm import get_cmap
# from matplotlib.colors import LogNorm
# import matplotlib.ticker as mticker
# import cartopy.crs as crs
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import numpy as np
# import cartopy.feature as cfeature
# import os

class Warfy:
    def __init__(self):
        self._vars = {}

    def load_var(self, file, var, plevel=None, zlevel=None):
        ds = wrf.getvar(netCDF4.Dataset(file),var,timeidx=wrf.ALL_TIMES)
        ds = ds.assign_coords({'lon': ds.XLONG.isel(south_north=0), 'lat':
            ds.XLAT.isel(west_east=0)})
        ds = ds.rename({'south_north':'lat', 'west_east':'lon', 'Time':'time'})
        ds.attrs['coordinates'] = 'time lat lon'
        ds = ds.drop('XTIME')

        self._vars[var] = ds

    def get_vars(self):
        return self._vars

    def set_xlim(self,lon_start,lon_end):
        variables = self._vars
        for var in variables:
            variables[var] = variables[var].sel(lon=slice(lon_start,lon_end))


test = Warfy()
test.load_var(file,'DUST_1')
test.set_xlim(110,150)
test.get_vars()['DUST_1'].lon['lon']

var = 'DUST_1'


# wrf.getvar(netCDF4.Dataset(file),'DUST_1',timeidx=wrf.ALL_TIMES)

file = 'D://thesisdata/wrf_dust/wrfout_d01_2009-09-18_00_00_00'

#%%

def loadvar(wrffile,varname,lons=(110.3,-170),lats = (-57.06,-9.5),
    units="kt",plevel=None,zlevel=None):
    """
    converts dataarrays from wrffile into right shape to plot with wrfplot()
    """
    iselstart = wrf.ll_to_xy(wrffile,lats[0],lons[0]).values
    iselend = wrf.ll_to_xy(wrffile,lats[1],lons[1]).values
    windvars = ['uvmet10','ua','va','wa','uvmet','wspd_wdir']
    u,v = None,None
    if (varname=='RAIN'):
        print('RAIN is not a valid variable! \n'+
            'However, i create it by adding (fill Nan with 0!)\n'+
            'Cumulus Precipitation and Grid Scale Prec.\n'+
            '(PREC_ACC_C+PREC_ACC_NC)')
        rainc = wrf.getvar(wrffile,'PREC_ACC_C',
            timeidx=wrf.ALL_TIMES).isel(
            west_east=slice(iselstart[0],iselend[0]),
            south_north=slice(iselstart[1],iselend[1])
            ).fillna(0)
        rainnc = wrf.getvar(wrffile,'PREC_ACC_NC',
            timeidx=wrf.ALL_TIMES).isel(
            west_east=slice(iselstart[0],iselend[0]),
            south_north=slice(iselstart[1],iselend[1])
            ).fillna(0)
        var = rainc.copy(deep=False)
        var.values = rainc + rainnc
        var.attrs['description'] = 'Total precipitation (acc. last 3h)'
    elif ((varname[-1] == '_')|(varname=='DUST_EMIS_ACC')):
        print('no explicit binsize\n'+
            'build sum over all binsizes 1-5! (fill NaN with 0!)')
        vars = [None]*5
        for binsize in range(5):
            vars[binsize] = wrf.getvar(wrffile,varname+str(binsize+1),
                timeidx=wrf.ALL_TIMES).isel(
                west_east=slice(iselstart[0],iselend[0]),
                south_north=slice(iselstart[1],iselend[1])
                ).fillna(0)
        var = vars[0].copy(deep=False)
        var.values = vars[0]+vars[1]+vars[2]+vars[3]+vars[4]
        if (varname=='DUST_'):
            var.attrs['description'] = 'Dust concentration (all binsizes)'
        else:
            var.attrs['description'] = var.description+'-5 (sum)'
    elif (varname in windvars):
        var = wrf.getvar(wrffile,varname,units=units,
        timeidx=wrf.ALL_TIMES).isel(
        west_east=slice(iselstart[0],iselend[0]),
        south_north=slice(iselstart[1],iselend[1])
        )
    else:
        var = wrf.getvar(wrffile,varname,
        timeidx=wrf.ALL_TIMES).isel(
        west_east=slice(iselstart[0],iselend[0]),
        south_north=slice(iselstart[1],iselend[1])
        )
    if ((len(var.shape)==4) & (var.shape[0]==97)):
        print ('4d variable with '+str(var.shape[1])+' heightlevels')
        if ((plevel!=None) & (zlevel==None)):
            p = wrf.getvar(wrffile,"pressure",timeidx=wrf.ALL_TIMES).isel(
            west_east=slice(iselstart[0],iselend[0]),
            south_north=slice(iselstart[1],iselend[1])
            )
            var_temp = wrf.interplevel(var,p,plevel)
            var = var[:,0,...].copy(deep=False)
            var.values = var_temp
            var.attrs['description'] = (var.description+'\n (at '
                +str(plevel)+'hPa)')
            cvar = var
        elif ((plevel==None) & (zlevel!=None)):
            var = var[:,zlevel,...]
            var.attrs['description'] = (var.description+'\n (at zlevel '
                +str(zlevel)+'/31)')
            cvar = var
        else:
            raise ValueError(
                '4D variable! Choose zlevel or interpolate to plevel')
        cvar = var
        vector=False
    elif ((len(var.shape)==4) & (var.shape[0]==2)):
        print ('3d variable as vector with u,v')
        u = var[0,:]
        v = var[1,:]
        cvar= np.sqrt(u**2+v**2)
        vector = True
    elif ((len(var.shape)==5) & (var.shape[0]==2)):
        print ('4d variable as vector with u,v and '+str(var.shape[2])+
        ' heightlevels')
        u = var[0,:]
        v = var[1,:]
        cvar= np.sqrt(u**2+v**2)
        vector = True
    elif ((len(var.shape)==3) & (var.shape[0]==97)):
        print ('3d variable')
        cvar = var
        vector = False
    return var, cvar, vector, u, v


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
