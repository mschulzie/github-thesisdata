import matplotlib.pyplot as plt
import numpy as np

fe = 3
sigma = 1
mu = 5
t = np.linspace(-10,10,1000)
p = fe / np.sqrt(2*np.pi*sigma**2) * np.exp(-((t-mu)**2/(2*sigma**2)))

plt.plot(t,p)
np.diff(t).size
x = p*np.diff(t)[0]
x.sum()
