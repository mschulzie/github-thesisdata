from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
import numpy as np
import cartopy.feature as cfeature
import wrf

#%%

def wrfplot(wrffile,varname,time='2009-09-18T00',units="kt",ppfig=(1,1),
    save=False,savedir=None,show=True,cmap='RdBu_r', qmin=0.7,
    qmax=0.99, levels=50,limmax=None):

    windvars = ['uvmet10','ua','va','wa','uvmet','wspd_wdir']

    if (varname[-1] == '_'):
        print('no explicit binsize, build sum over all binsizes 1-5!')
        vars = [None]*5
        for binsize in range(5):
            vars[binsize] = wrf.getvar(wrffile,varname+str(binsize+1),
                timeidx=wrf.ALL_TIMES)
            vars[binsize] = vars[binsize].isel(west_east=slice(0,143))
        var = vars[0].copy(deep=False)
        var.values = vars[0]+vars[1]+vars[2]+vars[3]+vars[4]
        var.attrs['description'] = var.description+'-5 (sum)'
    elif (varname in windvars):
        var = wrf.getvar(wrffile,varname,units=units,
        timeidx=wrf.ALL_TIMES).isel(west_east=slice(0,143))
    else:
        var = wrf.getvar(wrffile,varname,
        timeidx=wrf.ALL_TIMES).isel(west_east=slice(0,143))

    lats, lons = wrf.latlon_coords(var)
    cart_proj = wrf.get_cartopy(var)

    if ((len(var.shape)==4) & (var.shape[0]==97)):
        print ('4d variable with '+str(var.shape[1])+' heightlevels')
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

    #Computes the limits from which data should be shown by using quantiles
    limmin = cvar.quantile(qmin)
    if (limmax==None):
        limmax = (int(np.round(cvar.quantile(qmax),
            -len(str(int(cvar.quantile(qmax))))+4))) + 1
    c_levels = np.linspace(limmin,limmax,levels)

    #Computes ticks for colorbar
    cb_fontsize = 8
    cbar_min = int(np.round(limmin,-len(str(int(limmax)))+4))
    cbar_max = limmax - 1
    if ((cbar_max-cbar_min) > 10):
        cbar_step = int((cbar_max-cbar_min)/10)
    else:
        cbar_step = (cbar_max-cbar_min)/10
    cbarticks = np.arange(cbar_min, cbar_max+cbar_step,cbar_step)
    if (len(cbarticks)>levels):
        cbarticks = c_levels
    if (limmax < 99999):
        cbformat = '%d'
    else:
        cbformat = '%.1E'

    var = var.sel(Time=time)
    cvar = cvar.sel(Time=time)
    if vector:
        u = u.sel(Time=time)
        v = v.sel(Time=time)
    t=0
    while (t<var.Time.size):
    #for t in range(var.Time.size//(ppfig[0]*ppfig[1]+1)+1):
        fig = plt.figure(figsize=(5*ppfig[1],4*ppfig[0]))
        gs = fig.add_gridspec(ppfig[0],ppfig[1],hspace=0.4)
        count = 0
        for i in range(ppfig[0]):
            for j in range(ppfig[1]):
                ax = fig.add_subplot(gs[i,j], projection=cart_proj)
                ax.coastlines(lw=.5, zorder=5)
                ax.add_feature(cfeature.BORDERS, lw=.5, zorder=4)
                ax.add_feature(cfeature.LAND, fc='lightgrey', zorder=3)
                ax.add_feature(cfeature.STATES,lw=.2, zorder=3)
                if (var.Time.size > 1):
                    cvar_t = cvar.isel(Time=t+count)
                else:
                    cvar_t = cvar
                cvar_contour = ax.contourf(wrf.to_np(lons), wrf.to_np(lats),
                    wrf.to_np(cvar_t),
                    zorder=4, transform=crs.PlateCarree(),
                    cmap=cmap,alpha=1,levels=c_levels,extend='max')
                cb = plt.colorbar(cvar_contour, shrink=.98,
                    format=cbformat)
                cb.set_ticks(cbarticks)
                cb.ax.tick_params(labelsize=cb_fontsize)
                cb.set_label(label=(var.description+' in '+var.units),
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
                ax.set_xlim(wrf.cartopy_xlim(var))
                ax.set_ylim(wrf.cartopy_ylim(var))
                gl = ax.gridlines(
                    crs=crs.PlateCarree(), draw_labels=True,
                    linewidth=1, color='gray', linestyle='dotted',
                    xlocs=[120,135,150,165,180], zorder=6)
                gl.top_labels = False
                gl.right_labels = False
                zeitstr = str(cvar_t.Time.values)
                ax.set_title('WRF - '+varname+' - '+zeitstr[:13],
                    fontsize=10)#+' - '+str(plevel)+' hPa')
                count += 1
                if (t+count==var.Time.size):
                    break
            else:
                continue
            break
        if save:
            if (savedir==None):
                print('Give path to save figures!!')
            if (ppfig[0]*ppfig[1] > 1):
                zeitstr = 'multiple_'+str(ppfig[0])+'x'+str(ppfig[1])
            fig.savefig(savedir+'Python/wrfout/'+varname+'/'+zeitstr[:13]
                +'.png', dpi = 500)
        if show:
            plt.show()
        plt.close()
        t += ppfig[0]*ppfig[1]
    return var
