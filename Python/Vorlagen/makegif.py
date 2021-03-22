import imageio
import marcowhereareyou as mway
import os

wrfout, savedir = mway.gimmedirs()

savedir
variable = 'DUSTLOAD_'
path = savedir+'Python/wrfout/'+variable+'/'
filenames = os.listdir(path)

with imageio.get_writer(path+'Dustload.gif', mode='I',
    duration=0.1) as writer:
    for filename in filenames:
        if filename.endswith(('.png')):
            image = imageio.imread(path+filename)
            writer.append_data(image)
