import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dir = "D://thesisdata/bilder/wetter3de/10mwind/"

img=mpimg.imread(dir+'2009091800_7_au.gif')

imgplot = plt.imshow(img[200:472,200:570])
imgplot.axes.get_xaxis().set_visible(False)
imgplot.axes.get_yaxis().set_visible(False)
