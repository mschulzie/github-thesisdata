from netCDF4 import Dataset
import numpy as np

ncfile = Dataset("D://thesisdata/wrf_dust/2021-06-09/wrfout_d01_2009-09-18_00_00_00")
vars = ncfile.variables

# np.max(vars[var]) braucht viel Zeit!

f = open('varnames_neu.txt','w+')
f.write('Insgesamt ' + str(len(vars)) + ' Variablen: \n')
for var in ncfile.variables:
    if var == 'Times':
        f.write(str(vars[var].name)+'\n')
    else:
        f.write(
                str(vars[var].name)+';'+ str(vars[var].description) +
                ';' + str(np.max(vars[var]))+';'+
                str(len(vars[var].shape))+';'+
                str(vars[var].shape)+';'+str(vars[var].units)+'\n'
                    )
f.close()
