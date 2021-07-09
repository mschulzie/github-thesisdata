import xarray as xr
import helperlies as mway
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
import string
from Python.modeloutput.deposition_iron import sections
which= ['Nordost','Korall','Tasman','Süden','Südozean']
sections = {key: sections[key] for key in which}

iron = pd.read_csv('./Python/chlorophyll/csv/iron_section_means_timeseries.csv')
chl = pd.read_csv('./Python/chlorophyll/csv/chl_section_means_timeseries.csv')

add=''
filter = True
freq_min=0
freq_max=1/5
tres=5

#%%
# if filter:
#     for ort in sections:
#         data[chl[ort] = mway.filter_via_fft(chl[ort],freq_max=freq_max,freq_min=freq_min)
#         chl_err[ort] = mway.filter_via_fft(chl_err[ort],freq_max=freq_max,freq_min=freq_min)

# Now PLOTTING:
def format_ax(ax,ylim=True):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b'))
    ax.tick_params(axis='x', labelrotation=0)
    ax.legend(fontsize=6)
    ax.grid(axis='x')
    ax.set_xlim('2009-06-01','2009-12-31')
    ax.set_xticklabels('')
    if ylim:
        ax.set_ylim(0,1)
        ax.set_yticks(np.arange(0.2,1.2,0.2))
t = pd.date_range('2009-06-01','2009-12-31',freq='d')
t_iron = pd.date_range('2009-06-01','2009-12-31',freq='3h')
rows, cols = len(sections),2
fig = plt.figure(figsize=(10,rows*2.5))
gs = fig.add_gridspec(rows,1,hspace=0.1)

ax1,ax2,ax3,ax4 = {},{},{},{}
for i,ort in enumerate(sections):
    gs1 = gs[i].subgridspec(2,2,hspace=0.02,wspace=0.2,height_ratios=[3,1])
    ax1[ort]= (fig.add_subplot(gs1[:,0]))
    ax2[ort]= (fig.add_subplot(gs1[0,1]))
    ax3[ort]= (fig.add_subplot(gs1[1,1]))
    ax1[ort].plot(t,chl[ort+';'+'CHL'],color='#ff2e00',label=r'$\mu_C(t)$')
    ax1[ort].plot(t,chl[ort+';'+'CHL_mean'],label=r'$\mu_{C,cli}(t)$',color='#0037a1')
    ax1[ort].fill_between(t,chl[ort+';'+'CHL_percentile_3'],chl[ort+';'+'CHL_percentile_97'],label=r'$\mu_{q_{0.03}}(t)$, $\mu_{q_{0.97}}(t)$',
        color='#13e3be',facecolor='#c1fbf6')
    ax1[ort].fill_between(t,chl[ort+';'+'CHL']-chl[ort+';'+'CHL_error'],chl[ort+';'+'CHL']+chl[ort+';'+'CHL_error'],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    ax1[ort].fill_between(t,chl[ort+';'+'CHL_mean']-chl[ort+';'+'CHL_standard_deviation'],
        chl[ort+';'+'CHL_mean']+chl[ort+';'+'CHL_standard_deviation'],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    format_ax(ax1[ort])
    ax1[ort].text(pd.to_datetime('2009-06-03'),0.98,
        '{:}° bis {:}° E und {:}° bis {:}° S\n({:})'.format(
        sections[ort][0],sections[ort][1],sections[ort][2]*-1,sections[ort][3]*-1,ort),
        va='top',bbox={'facecolor': 'white', 'alpha': .8, 'pad': 1})
    #RECHTE SEITE:
    chl_ano = chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']
    if filter:
        chl_ano = mway.filter_via_fft(chl_ano,freq_max=freq_max,freq_min=freq_min)
    ax2[ort].plot(t,chl_ano,color='#ff2e00',
        label=r'$\Delta \mu_C (t)$')
    ax2[ort].fill_between(t,chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']-chl[ort+';'+'CHL_error'+'_5'],
        chl[ort+';'+'CHL'+'_5']-chl[ort+';'+'CHL_mean'+'_5']+chl[ort+';'+'CHL_error'+'_5'],
        color='#9d1c3f',facecolor='#fbe0f9',label=r'$\mu_{\Delta C}(t)$')
    ax2[ort].fill_between(t,-chl[ort+';'+'CHL_standard_deviation'+'_5'],chl[ort+';'+'CHL_standard_deviation'+'_5'],
        color='#0094ff',facecolor='#b0d9fb',label=r'$\mu_\sigma (t)$',
        alpha=.5)
    ax3[ort].plot(t_iron,iron[ort],
        label=r'$F_{Fe}$',color='#525252')
    ax3[ort].set_yscale('log')
    ax3[ort].yaxis.set_label_position("right")
    ax3[ort].yaxis.tick_right()
    ax3[ort].set_yticks([1e-8,1e-5,1e-3])
    format_ax(ax2[ort],ylim=False)
    format_ax(ax3[ort],ylim=False)
    ax3[ort].set_ylim(1e-8,7e-3)
    ax1[ort].text(1.02, 0.5, string.ascii_uppercase[i], transform=ax1[ort].transAxes,
            size=20, weight='bold')
if filter:
    add+='_filter_{:}_{:}'.format(freq_min,freq_max)
ax1[list(sections)[0]].set_title('Rohdaten uneingeschränkt')
ax2[list(sections)[0]].set_title(r'Trend bereinigt und $m_{Fe}/A>$'+'{:.1f} ug/m2'.format(
    tres))
ax1[list(sections)[len(sections)//2]].set_ylabel('CHL-a Konzentrationen in mg/m3',fontsize=12)
ax1[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax1[list(sections)[-1]].tick_params(axis='x', labelrotation=0)
ax3[list(sections)[-1]].xaxis.set_major_formatter(mdates.DateFormatter('1.%b'))
ax3[list(sections)[-1]].tick_params(axis='x', labelrotation=0)
# ADD QUALITY EVENTS (FROM SATELLITE IMAGES)
ax3['Tasman'].annotate('12.09.',('2009-09-12T00',1e-8),
    xytext=('2009-09-12T00',1e-4),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')
ax3['Tasman'].annotate('13.10.',('2009-10-13T04',1e-8),
    xytext=('2009-10-13T04',1e-4),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')
ax3['Korall'].annotate('13.10.',('2009-10-13T04',1e-8),
    xytext=('2009-10-13T04',1e-4),textcoords='data',
    arrowprops={'arrowstyle':'->','color':'blue'},ha='center',fontsize=7,color='b')

plt.tight_layout()
fig.savefig('./Thesis/bilder/timeseries_all_without_coast'+add+'.png'
        ,dpi=200,facecolor='white',
        bbox_inches = 'tight',pad_inches = 0.01)
plt.show()
