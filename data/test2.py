import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D

def twoDimPlot (x, y, xLab = None, yLab = None, color = None, pointSize = 40):
    # Make plot
    marker = 'o'
    if color:
        plt.scatter(x, y, c=color, marker=marker, edgecolors='none', s=pointSize)
    else:
        plt.scatter(x, y, marker=marker, edgecolors='none', s=pointSize)

    # Add labels
    if xLab:
        plt.xlabel(xLab)
    if yLab:
        plt.ylabel(yLab)

    plt.show()

# Argument dict: label -> vals
def threeDimPlot (xyzDict, color = None, pointSize = 40):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    [xi, yi, zi] = list(xyzDict.keys())
    if color:
        ax.scatter(xyzDict[xi], xyzDict[yi], xyzDict[zi], c = color, edgecolors='none', s=pointSize)
    else:
        ax.scatter(xyzDict[xi], xyzDict[yi], xyzDict[zi], edgecolors='none', s=pointSize)

    ax.set_xlabel(xi)
    ax.set_ylabel(yi)
    ax.set_zlabel(zi)

    plt.show()

# Mutates list
# "a","b","a","c" -> 0,1,0,2
def labelsToIndices (labels):

    # Build dict
    nextKey = 0
    labelToIndex = {}
    for l in labels:
        if l not in labelToIndex:
            labelToIndex[l] = nextKey
            nextKey += 1

    # Update labels
    for i in range(0,len(labels)):
        labels[i] = labelToIndex[labels[i]]

x = [1,2,3,4]
y = [2,4,9,16]
z = [1,2,3,4]
xyzDict = {0:z,1:y,2:z}
color=["a","b","c","a"]
labelsToIndices(color)
threeDimPlot(xyzDict,color)
