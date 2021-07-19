import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import string

path = 'D://thesisdata/ice_cores/'

def normalize(col):
    return (col-col.min())/(col.max()-col.min())

iron = pd.read_csv(path+'taldice2013fe.txt',header=7,comment='#',sep='\t')
iron['time'] = iron['age_calkaBP']

co2_2015 = pd.read_csv(path+'antarctica2015co2composite.txt',
    delim_whitespace=True, comment='#')
co2_2015['time'] = co2_2015['age_gas_calBP'] *1e-3

#alter Datensatz aus 2008:
# dome_co2 = pd.read_csv(path+'edc-co2-2008_composite.txt',
#     header=91,delim_whitespace=True)
# dome_co2['time'] = dome_co2['Age(yrBP)'] * 1e-3

dust_2012 = pd.read_csv(path+'edc2012dust.txt',header=74,delim_whitespace=True,
    encoding='latin1')
dust_2012['time'] = dust_2012['EDC3Age(kyrBP)']

#älterer Datensatz aus 2008:
# dome_dust = pd.read_csv(path+'edc-dust2008_clean.txt',
#     header=6,delim_whitespace=True).drop(
#     columns='Depth(m)')
# dome_dust['time'] = dome_dust['EDC3Age(kyrBP)']

dome_ch4 = pd.read_csv(path+'edc-ch4-2008_clean.txt',
    header=0,delim_whitespace=True).drop(
    columns=['Depth','Lab.','1s'])
dome_ch4['time'] = dome_ch4['Gas_Age'] * 1e-3

dome_temp = pd.read_csv(path+'edc3deuttemp2007_clean.txt',
    header=0,delim_whitespace=True).drop(
    columns=['ztop','Bag','Deuterium'])
dome_temp['time'] = dome_temp['Age'] * 1e-3

fig = plt.figure(figsize=(8,4))
gs = fig.add_gridspec(4,1,hspace=0)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[3])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[1])
co2_2015
ax1.plot(co2_2015['time'],co2_2015['co2_ppm'],
    color='black',label='Komposit CO2')
ax4.plot(dome_temp['time'],dome_temp['Temperature'],
    color='indianred',label='Temperatur (berechnet)')
ax3.plot(dome_ch4['time'],dome_ch4['CH4_mean'],
    color='cornflowerblue',label='CH4')
ax2.plot(dust_2012['time'],np.log10(dust_2012['DustFlux(mg/m2/a)']),
    color='darkorange',label='Staub Fluss',linewidth=.4)
#fig.suptitle('EPICA Dome C Ice Core 800KYr')
ax1.grid(axis='x'), ax2.grid(axis='x'), ax3.grid(axis='x'), ax4.grid(axis='x')
ax1.axes.set_xticklabels(''), ax4.axes.set_xticklabels('')
ax3.axes.set_xticklabels('')
labelsize = 10
legendsize = 10
ax1.set_ylabel('ppmv',fontsize=labelsize,labelpad=6)
ax4.set_ylabel('°C',fontsize=labelsize,labelpad=5)
ax3.set_ylabel('ppbv',fontsize=labelsize,labelpad=6)
ax2.set_ylabel('log10\nmg/m2/a',fontsize=labelsize,labelpad=6)
#plt.tight_layout()
ax1.legend(fontsize=legendsize,loc='upper right')
ax2.legend(fontsize=legendsize,loc='upper right')
ax3.legend(fontsize=legendsize,loc='upper right')
ax4.legend(fontsize=legendsize,loc='upper right')
ax2.set_xlabel('Zeit in tausend Jahren vor heute ')
ax1.set_xlim(0,800),ax2.set_xlim(0,800),ax3.set_xlim(0,800),ax4.set_xlim(0,800)
ax1.text(0.01,0.75,'A',transform=ax1.transAxes,weight='bold',size=15)
ax2.text(0.01,0.75,'D',transform=ax2.transAxes,weight='bold',size=15)
ax3.text(0.01,0.75,'C',transform=ax3.transAxes,weight='bold',size=15)
ax4.text(0.01,0.75,'B',transform=ax4.transAxes,weight='bold',size=15)
plt.tight_layout()
plt.savefig('./Thesis/bilder/epica_icecore.pdf',
    bbox_inches='tight',pad_inches=0.01,facecolor='white')
plt.show()
#plt.close()
#%%
fig = plt.figure(figsize=(7,2))
ax = fig.add_subplot(111)

iron_log = np.log10(iron['Fe flux'])
iron_norm = normalize(iron_log)
co2_2015_red = co2_2015[co2_2015['time']>0]
co2_2015_red = co2_2015_red[co2_2015_red['time']<314]
co2_2015_red
co2_norm = normalize(co2_2015_red['co2_ppm'])

ax.plot(iron['time'],iron_norm,label='Eisen Fluss (log10)',color='darkred')
ax.plot(co2_2015_red['time'],co2_norm,label='CO2 Konz.',color='black')
#plt.plot(dome_dust['time'],normalize((dome_dust['LaserDust(ng/g)'])),label='dust')
#plt.plot(iron['time'],normalize(iron['Fe flux']),label='iron flux')
ax.set_xlabel('Zeit in tausend Jahren vor heute ')
ax.set_ylabel('Normalisierte Skala')
ax.legend(loc='upper right',framealpha=.5,fontsize=10)
ax.grid(axis='x')
ax.set_xlim(-1,314)
ax.set_yticklabels('')
#fig.suptitle('CO2 Komposit vs. Eisen Fluss Talos Dome Eiskern')
fig.savefig('./Thesis/bilder/co2_iron.pdf',
        bbox_inches='tight',pad_inches=0.01,facecolor='white')
plt.show()
