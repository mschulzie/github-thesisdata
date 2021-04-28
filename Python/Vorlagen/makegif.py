import imageio
import helperlies as mway
import os

wrfout, savedir = mway.gimmedirs()

savedir
variable = 'DUSTLOAD_-DUST_EMIS_ACC'
path = savedir+'Python/wrfout/'+variable+'/'
filenames = os.listdir(path)

with imageio.get_writer(path+'Dustload_Emis.gif', mode='I',
    duration=0.1) as writer:
    for filename in filenames:
        if filename.endswith(('.png')):
            image = imageio.imread(path+filename)
            writer.append_data(image)
