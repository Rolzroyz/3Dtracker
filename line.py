import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# start figure 1 with 3D plot
fig = plt.figure(1)
ax = fig.gca(projection='3d')

# legend
#mpl.rcParams['legend.fontsize'] = 10

#p1 = ax.scatter(0, 0, 1, c='b', label='woo')
#p2 = ax.scatter(0,1,0, c='g', label='woo2')
#plt.legend((p1, p2), ('woo','woo2'),loc=1)
#p = Rectangle((0, 0), 1, 1, fc="r")
#legend([p], ["Red Rectangle"])


# plot 3D line
x = np.linspace(2,3,100)
y = np.linspace(2,3,100)
z = np.linspace(2,3,100)
ax.plot(x, y, z)
#ax.legend(('line fit','red','blue'))
ax.legend(bbox_to_anchor=(0, 0, 1, 1))

# plot 3D scatter
ax.scatter(0,0,0,c=[.1,.1,1],marker='o',label='woo')
ax.scatter(1,1,1,c='c',marker='o',label='woo2')
#p1=ax.scatter(2,2,2,c='b',marker='o',label='somethin')
#p2=ax.scatter(3,3,3,c='g',marker='o',label='somethin else')
#ax.scatter(4,4,4,c='y',marker='o')
#ax.legend()
#p1, = plot([1,2,3])
#p2, = plot([3,2,1])
#p3, = plot([2,3,1])
#ax.legend([p2, p1], ["line 2", "line 1"])


# =============
# plot in different colors
# 'y' yellow
# 'b' blue
# 'g' green
# 'c' cyan
# 'm' magenta
# [R,G,B] values b/w 0 and 1

# ============
# to plot specific figures... also subplots!:
plt.figure(2)
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)
#subplots
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')

# ============
plt.show()

# =====================================================

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure(3)
ax = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.show()
