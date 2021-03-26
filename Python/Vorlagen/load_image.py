import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

dir1 = "D://thesisdata/bilder/Python/wrfout/RAIN/"
dir2 = "D://thesisdata/bilder/Python/era5/tp/"

shape = [4,8]

files1 = os.listdir(dir1)
files2 = os.listdir(dir2)
k=0
while (k< len(files)):
    fig = plt.figure(figsize=(26,14))
    gs = fig.add_gridspec(shape[0],shape[1],hspace=0.,wspace=0.1)
    count = 0
    for i in range(shape[1]):
        ax1 = fig.add_subplot(gs[0,i])
        ax2 = fig.add_subplot(gs[1,i])
        ax1.imshow(mpimg.imread(dir1+files1[k+count])[:,100:-200])
        ax2.imshow(mpimg.imread(dir2+files2[k+count])[:,100:-200])
        ax1.axis('off')
        ax2.axis('off')
        count += 1
    for i in range(shape[1]):
        ax1 = fig.add_subplot(gs[2,i])
        ax2 = fig.add_subplot(gs[3,i])
        ax1.imshow(mpimg.imread(dir1+files1[k+count])[:,100:-200])
        ax2.imshow(mpimg.imread(dir2+files2[k+count])[:,100:-200])
        ax1.axis('off')
        ax2.axis('off')
        count += 1
    k+= count
    fig.savefig('D://thesisdata/bilder/compare/'+
        'WRF_vs_er5_RAIN_'+str(k)+'.png',dpi=500)
