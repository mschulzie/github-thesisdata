import os

savedir = 'D://thesisdata/plankton/monthly/'
os.chdir(savedir)


for file in os.listdir():
    os.rename(file, file[3:7]+'_'+file[:2]+'_GMIS_A_CHLA.nc')
