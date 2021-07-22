import xarray as xr
import helperlies as mway
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
import string
from Python.modeloutput.deposition_iron import sections
which= ['Nordwest','Korall','Tasman','Süden','Südozean']
sections = {key: sections[key] for key in which}

iron = pd.read_csv('./Python/chlorophyll/csv/iron_section_means_timeseries.csv')
chl = pd.read_csv('./Python/chlorophyll/csv/chl_section_means_timeseries.csv')


filter = True
freq_min=0
freq_max=1/10
tres=5

#%%
add=''
# if filter:
#     for ort in sections:
#         data[chl[ort] = mway.filter_via_fft(chl[ort],freq_max=freq_max,freq_min=freq_min)
#         chl_err[ort] = mway.filter_via_fft(chl_err[ort],freq_max=freq_max,freq_min=freq_min)

# Now PLOTTING:
def format_ax(ax,ylim=True):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
    ax.tick_params(axis='x', labelrotation=0)
    #ax.legend(fontsize=6)
    ax.grid(axis='x')
    ax.set_xlim('2009-06-01','2009-12-31')
    ax.set_xticklabels('')
    if ylim:
        ax.set_ylim(0,.8)
        ax.set_yticks(np.arange(0.2,1.0,0.2))
        for label in ax.yaxis.get_ticklabels():
            label.set_verticalalignment('top')
    ax.tick_params(axis="y",direction="in")
t = pd.date_range('2009-06-01','2009-12-31',freq='d')
t_iron = pd.date_range('2009-06-01','2009-12-31',freq='3h')
rows, cols = len(sections),2
fig = plt.figure(figsize=(10,rows*2.5))
gs = fig.add_gridspec(rows,1,hspace=0.02)

ax1,ax2,ax3,ax4 = {},{},{},{}
for i,ort in enumerate(sections):
    gs1 = gs[i].subgridspec(2,2,hspace=0.02,wspace=0.12,height_ratios=[3,1])
    ax1[ort]= (fig.add_subplot(gs1[:,0]))
    ax2[ort]= (fig.add_subplot(gs1[0,1]))
    ax3[ort]= (fig.add_subplot(gs1[1,1]))
    im_chl, = ax1[ort].plot(t,chl[ort+';'+'CHL'],color='#ff2e00',label=r'$\mu_C(t)$')
    im_mean, = ax1[ort].plot(t,chl[ort+';'+'CHL_mean'],label=r'$\mu_{C,cli}(t)$',color='#0037a1')
    im_perz = ax1[ort].fill_between(t,chl[ort+';'+'CHL_percentile_3'],chl[ort+';'+'CHL_percentile_97'],label=r'$\mu_{q_{0.03}}(t)$, $\mu_{q_{0.97}}(t)$',
        color='#13e3be',facecolor='#c1fbf6')
    im_err = ax1[ort].fill_between(t,chl[ort+';'+'CHL']-chl[ort+';'+'CHL_error'],chl[ort+';'+'CHL']+chl[ort+';'+'CHL_error'],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    im_std = ax1[ort].fill_between(t,chl[ort+';'+'CHL_mean']-chl[ort+';'+'CHL_standard_deviation'],
        chl[ort+';'+'CHL_mean']+chl[ort+';'+'CHL_standard_deviation'],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    format_ax(ax1[ort])
    ax1[ort].text(0.99,.98,
        '{:}-{:}°E, {:}-{:}°S\n({:})'.format(
        sections[ort][0],sections[ort][1],sections[ort][2]*-1,sections[ort][3]*-1,ort),
        va='top',bbox={'facecolor': 'white', 'alpha': .8, 'pad': 1},ha='right',
        transform=ax1[ort].transAxes)
    #RECHTE SEITE:
    chl_ano = chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']
    im_chl_t, = ax2[ort].plot(t,chl_ano,color='#ff2e00',
        label=r'$\Delta \mu_C (t)$')
    if filter:
        chl_ano = mway.filter_via_fft(chl_ano,freq_max=freq_max,freq_min=freq_min)
        im_filt, = ax2[ort].plot(t,chl_ano,color='black',linestyle='dotted',linewidth=1,
            label=r'$\Delta \mu_C (t)$ mit $f_{max}$='+str(freq_max)+'/day')
    im_err_t = ax2[ort].fill_between(t,chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']-chl[ort+';'+'CHL_error'+'_5'],
        chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']+chl[ort+';'+'CHL_error'+'_5'],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    im_std_t = ax2[ort].fill_between(t,-chl[ort+';'+'CHL_standard_deviation'+'_5'],chl[ort+';'+'CHL_standard_deviation'+'_5'],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    im_iron, = ax3[ort].plot(t_iron,iron[ort],
        label=r'$F_{Fe}$',color='#525252')
    ax3[ort].set_yscale('log')
    ax3[ort].yaxis.set_label_position("right")
    ax3[ort].yaxis.tick_right()
    ax3[ort].set_yticks([1e-8,1e-5,1e-3])
    format_ax(ax2[ort],ylim=False)
    format_ax(ax3[ort],ylim=False)
    ax3[ort].set_ylim(1e-8,7e-3)
    ax1[ort].text(-0.15, 0.5, string.ascii_uppercase[i], transform=ax1[ort].transAxes,
            size=20, weight='bold',ha='right')
if filter:
    add+='_filter_{:}_{:}'.format(freq_min,freq_max)
ax1[list(sections)[0]].set_title('Rohdaten uneingeschränkt')
ax2[list(sections)[0]].set_title(r'Trend bereinigt und $\int F_{Fe} dt>$'+'{:.1f} ug/m2'.format(
    tres))
ax1[list(sections)[len(sections)//2]].set_ylabel('CHL-a Konzentrationen in mg/m3',fontsize=12)
ax1[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax1[list(sections)[-1]].tick_params(axis='x', labelrotation=0)
ax3[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax3[list(sections)[-1]].tick_params(axis='x', labelrotation=0)
# ADD QUALITY EVENTS (FROM SATELLITE IMAGES)
ax3['Tasman'].annotate('12.09.',('2009-09-12T00',1e-8),
    xytext=('2009-09-12T00',1e-5),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')
ax3['Tasman'].annotate('13.10.',('2009-10-13T04',1e-8),
    xytext=('2009-10-13T04',1e-5),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')
ax3['Tasman'].annotate('1.10.',('2009-10-01T12',1e-8),
    xytext=('2009-10-01T12',2e-4),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')
ax3['Korall'].annotate('13.10.',('2009-10-13T04',1e-8),
    xytext=('2009-10-13T04',1e-4),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')

leg1 = ax1['Nordwest'].legend([im_chl,im_err,im_std,im_mean,im_perz],[
    r'$\mu_C(t)$ Rohdaten',
    r'$\mu_{\Delta C}(t)$ Fehler',r'$\mu_\sigma (t)$ Std.abw.',
    r'$\mu_{C,cli}(t)$ Klima-MW',r'$\mu_{q_{0.03}}(t)$, $\mu_{q_{0.97}}(t)$'],loc='upper left',
    borderaxespad=0.02,fontsize=8,title_fontsize=8)
leg2 = ax2['Nordwest'].legend([im_chl_t,im_err_t,im_std_t,im_filt],[
    r'$\Delta \mu_C (t)$ Anomalie',
    r'$\mu_{\Delta C}(t)$ Fehler',r'$\mu_\sigma (t)$ Std.abw.',
    r'$\Delta \mu_C (t); \ f_{max}$='+str(freq_max)+'/d'],
    loc='upper left',borderpad=0.4,
    borderaxespad=0.02,fontsize=8,title_fontsize=8)
leg3 = ax3['Nordwest'].legend([im_iron],[r'$F_{Fe}$ in µg/m2/s'],loc='upper left',
    borderpad=0.4,borderaxespad=0.02,fontsize=8,title_fontsize=8)
ax2['Südozean'].set_yticklabels('')
ax2['Südozean'].text(0.5,0.5,'Keine Werte, Eintrag < 5 µg/m2',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 3},ha='center',
   va='center',transform=ax2['Südozean'].transAxes)
#ax2['Südozean'].add_artist(leg1)

plt.tight_layout()
fig.savefig('./Thesis/bilder/timeseries_all.png'
        ,dpi=300,
        bbox_inches = 'tight',pad_inches = 0.01)
plt.show()
