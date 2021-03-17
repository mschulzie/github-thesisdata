import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dir = "D://thesisdata/bilder/wetter3de/10mwind/"

img=mpimg.imread('http://www.bom.gov.au/cgi-bin/charts/charts.view.pl?idcode=IDX0102&file=IDX0102.200909181200.gif')

imgplot = plt.imshow(img[200:472,200:570])
imgplot.axes.get_xaxis().set_visible(False)
imgplot.axes.get_yaxis().set_visible(False)


from PIL import Image
import requests
from io import BytesIO

url = 'http://www.bom.gov.au/cgi-bin/charts/charts.view.pl?idcode=IDX0102&file=IDX0102.200909181200.gif'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
