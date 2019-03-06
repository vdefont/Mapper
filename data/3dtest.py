# Run using python3

import numpy as np
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import csv

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100

x = []
y = []
z = []
with open('./toy/fourComponents/points.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[2]))
        y.append(float(row[3]))
        z.append(float(row[4]))

for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    ax.scatter(x, y, z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
