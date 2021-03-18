import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dir = "D://thesisdata/bilder/wetter3de/10mwind/"
filename = 'iein Name'

img=mpimg.imread(dir+filename)

imgplot = plt.imshow(img[200:472,200:570])
imgplot.axes.get_xaxis().set_visible(False)
imgplot.axes.get_yaxis().set_visible(False)
