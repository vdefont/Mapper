import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D

import util

# Default file names for points and evecs
POINTS_FILENAME = "points.csv"
EVECS_FILENAME = "evecs.csv"
DEFAULT_POINT_SIZE = 10

def twoDimPlot (x, y, xLab = None, yLab = None, color = None, pointSize = DEFAULT_POINT_SIZE):
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
def threeDimPlot (xyzDict, color = None, pointSize = DEFAULT_POINT_SIZE):
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


def printInstructions ():
    print("Please follow this format:")
    print("<dataFile>")
    print(" -cols <col1> <col2> (<col3>)")
    print(" -color <colorFile> (OPTIONAL)")
    print("  example: points.csv -cols 0 1")
    print("  example: points.csv -color colors.csv -cols 1 2 3")

args = util.parseArgs(sys.argv, firstArg = "file", requiredArgs = ["file", "cols"])
if not args: # Invalid args
    printInstructions()
else:
    # Get data from args
    evecsFile = args["file"][0]
    if "color" in args:
        colorFile = args["color"][0]
    else:
        colorFile = None
    colIndices = args["cols"]
    util.toIntArray(colIndices)

    # Set up dict of evecs
    cols = util.readColsFromFile(evecsFile, colIndices)

    color = None
    if colorFile:
        color = util.readColFromFile(colorFile, 0)
        util.labelsToIndices(color)

    if len(colIndices) == 2:
        [aIndex, bIndex] = colIndices
        twoDimPlot(cols[aIndex], cols[bIndex], xLab=aIndex, yLab=bIndex, color=color)
    elif len(colIndices) == 3:
        threeDimPlot(cols, color=color)
    else:
        printInstructions()
