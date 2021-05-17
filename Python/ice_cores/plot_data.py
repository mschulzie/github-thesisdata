import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

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

dust_2012 = pd.read_csv(path+'edc2012dust.txt',header=74,delim_whitespace=True)
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
ax1 = fig.add_subplot(411)
ax2 = fig.add_subplot(414)
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(412)
co2_2015
ax1.plot(co2_2015['time'],co2_2015['co2_ppm'],
    color='black',label='Composite CO2 record')
ax4.plot(dome_temp['time'],dome_temp['Temperature'],
    color='indianred',label='Estimate (diff. average of last 1000 years)')
ax3.plot(dome_ch4['time'],dome_ch4['CH4_mean'],
    color='cornflowerblue',label='mean')
ax2.plot(dust_2012['time'],np.log10(dust_2012['DustFlux(mg/m2/a)']),
    color='darkorange',label='EPICA Dome C Ice Core Dust Flux Data')
dust_2012
fig.suptitle('EPICA Dome C Ice Core 800KYr')
ax1.grid(axis='x'), ax2.grid(axis='x'), ax3.grid(axis='x'), ax4.grid(axis='x')
ax1.axes.set_xticklabels(''), ax4.axes.set_xticklabels('')
ax3.axes.set_xticklabels('')
labelsize = 10
legendsize = 8
ax1.set_ylabel('CO2\nppmv',fontsize=labelsize,labelpad=11)
ax4.set_ylabel('Temp.',fontsize=labelsize,labelpad=8)
ax3.set_ylabel('CH4\nppbv',fontsize=labelsize,labelpad=9)
ax2.set_ylabel('log10\nDustFlux\nmg/m2/a',fontsize=labelsize,labelpad=10)
#plt.tight_layout()
ax1.legend(fontsize=legendsize)
ax2.legend(fontsize=legendsize)
ax3.legend(fontsize=legendsize)
ax4.legend(fontsize=legendsize)
ax2.set_xlabel('Zeit in tausend Jahren vor heute ')

plt.tight_layout()
plt.savefig('D://thesisdata/bilder/Python/epica_icecore.png',dpi=500)
plt.show()
plt.close()
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
ax.legend(loc='upper right',framealpha=.5)
ax.grid(axis='x')
ax.set_xlim(-1,314)
ax.set_yticklabels('')
fig.suptitle('CO2 Komposit vs. Eisen Fluss Talos Dome Eiskern')
fig.savefig('D://thesisdata/bilder/Python/co2_iron.png',dpi=300)
plt.show()
