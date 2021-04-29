import helperlies as mway
import matplotlib.pyplot as plt
import numpy as np

#1: '#d62323','#b4622d','#1473c1','#471d70','#d62323'

cmap = mway.make_segmented_cmap(
    '#d62323','#b4622d','#1473c1','#471d70','#d62323')

# schwarz, orange, braun, rot

x = np.linspace(-np.pi,np.pi,1000)
y = np.linspace(-0.5,0.5,200)

X,Y = np.meshgrid(x,y)
X.shape
fig = plt.figure(figsize=(8,8))
gs = fig.add_gridspec(2,1,hspace=0.5,height_ratios=[1,4])
ax = fig.add_subplot(gs[0,0])

ax.contourf(X,Y,X,cmap=cmap,levels=100)
ax.set_xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi])
ax.set_yticks([])
ax.set_xticklabels([r'-$\pi$',r'-$\pi/2$','0',r'$\pi/2$',r'$\pi$'],fontsize=15)
ax.set_ylim(-0.5,0.5)
ax.set_yticklabels('')

ax1 = fig.add_subplot(gs[1,0],projection='polar')
r = np.linspace(0.6,1,100)
theta = np.linspace(0,2*np.pi,100)
R,THETA = np.meshgrid(r, theta)

ax1.contourf(THETA,R,THETA,100,cmap=cmap)
ax1.set_yticks([])
ax1.set_rorigin(0)
ax1.set_theta_zero_location('E', offset=0)
step = np.pi/4
ax1.set_xticks(np.arange(0,2*np.pi,step))
ax1.set_xticklabels([r'$\pi$',r'$-\frac{3}{4}\pi$',r'$-\frac{1}{2}\pi$',
    r'$-\frac{1}{4}\pi$','0',r'$\frac{1}{4}\pi$',r'$\frac{1}{2}\pi$',
    r'$\frac{3}{4}\pi$'],fontsize=15)

plt.show()
