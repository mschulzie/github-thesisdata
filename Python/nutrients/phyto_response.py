import matplotlib.pyplot as plt
import numpy as np

fe = 3
sigma = 0.3
mu = 5
t = np.linspace(0,10,1000)
p = fe / np.sqrt(2*np.pi*sigma**2) * np.exp(-((t-mu)**2/(2*sigma**2)))

plt.plot(t,p)
plt.xticks(np.arange(0,10,1))
np.diff(t).size
x = p*np.diff(t)[0]
x.sum()
dust_radius = [0.5,1.4,2.4,4.5,8.0]
sinking(1e6)
def sinking(d):
    d = d*1e-6
    rho_particle = 1490
    rho_water = 1025
    g = 9.81
    mu = 1e-3 #fluid dynamic viscosity of seawater
    return 1/18 * (g*(rho_particle-rho_water)*d**2)/(mu)
