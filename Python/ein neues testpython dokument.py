import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-20,20,1000)
y = x**3 + 5*x**2 + 10*x + 1

# na hier fehlte aber noch ein cleverer Kommentar!

plt.plot(x,y)
