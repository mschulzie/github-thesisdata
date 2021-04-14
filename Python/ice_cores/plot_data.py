import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

path = 'D://thesisdata/ice_cores/'

iron = pd.read_csv(path+'taldice2013fe.txt',header=7,comment='#',sep='\t')

dome_co2 = pd.read_csv(path+'edc-co2-2008_composite.txt',
    header=91,delim_whitespace=True)
dome_co2['time'] = dome_co2['Age(yrBP)'] * 1e-3

dome_dust = pd.read_csv(path+'edc-dust2008_clean.txt',
    header=6,delim_whitespace=True).drop(
    columns='Depth(m)')
dome_dust['time'] = dome_dust['EDC3Age(kyrBP)']

dome_ch4 = pd.read_csv(path+'edc-ch4-2008_clean.txt',
    header=0,delim_whitespace=True).drop(
    columns=['Depth','Lab.','1s'])
dome_ch4['time'] = dome_ch4['Gas_Age'] * 1e-3

dome_temp = pd.read_csv(path+'edc3deuttemp2007_clean.txt',
    header=0,delim_whitespace=True).drop(
    columns=['ztop','Bag','Deuterium'])
dome_temp['time'] = dome_temp['Age'] * 1e-3

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(411)
ax2 = fig.add_subplot(414)
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(412)

ax1.plot(dome_co2['time'],dome_co2['CO2(ppmv)'],
    color='black',label='Composite CO2 record')
ax4.plot(dome_temp['time'],dome_temp['Temperature'],
    color='indianred',label='Estimate (diff. average of last 1000 years)')
ax3.plot(dome_ch4['time'],dome_ch4['CH4_mean'],
    color='cornflowerblue',label='mean')
ax2.plot(dome_dust['time'],dome_dust['LaserDust(ng/g)'],
    color='darkorange',label='EDC Coulter Counter dust mass concentration')

fig.suptitle('EPICA Dome C Ice Core 800KYr')
ax1.grid(axis='x'), ax2.grid(axis='x'), ax3.grid(axis='x'), ax4.grid(axis='x')
ax1.axes.set_xticklabels(''), ax4.axes.set_xticklabels('')
ax3.axes.set_xticklabels('')
labelsize = 10
legendsize = 8
ax1.set_ylabel('CO2(ppmv)',fontsize=labelsize,labelpad=11)
ax4.set_ylabel('Temperature',fontsize=labelsize,labelpad=8)
ax3.set_ylabel('CH4 (ppbv)',fontsize=labelsize,labelpad=9)
ax2.set_ylabel('CCDust(ng/g)',fontsize=labelsize,labelpad=3)
#plt.tight_layout()
ax1.legend(fontsize=legendsize)
ax2.legend(fontsize=legendsize)
ax3.legend(fontsize=legendsize)
ax4.legend(fontsize=legendsize)
ax2.set_xlabel('Zeit in tausend Jahren vor heute ')

plt.tight_layout()
plt.savefig('D://thesisdata/bilder/Python/epica_icecore.png',dpi=500)
plt.show()
