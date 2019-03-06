import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D

# Default file names for points and evecs
POINTS_FILENAME = "points.csv"
EVECS_FILENAME = "evecs.csv"

# Populates dict: index -> vals
def readColsFromFile (fileName, colsDict):

    # Read from file to populate dict
    with open(fileName, 'r') as csvFile:
        # Read each row
        rows = csv.reader(csvFile, delimiter=',')
        for row in rows:
            for colIndex in colsDict:
                colIndex = int(colIndex)
                colsDict[colIndex].append(float(row[colIndex]))

def twoDimPlot (x, y, xLab = None, yLab = None, color = None):
    # Make plot
    if color:
        plt.scatter(x, y, c=color)
    else:
        plt.scatter(x, y)

    # Add labels
    if xLab:
        plt.xlabel(xLab)
    if yLab:
        plt.ylabel(yLab)

    plt.show()

# Argument dict: label -> vals
def threeDimPlot (xyzDict):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    [xi, yi, zi] = list(xyzDict.keys())
    ax.scatter(xyzDict[xi], xyzDict[yi], xyzDict[zi])

    ax.set_xlabel(xi)
    ax.set_ylabel(yi)
    ax.set_zlabel(zi)

    plt.show()

args = sys.argv
numArgs = len(args) - 1
if numArgs < 1 or numArgs > 4:
    print("Must input 1 to 4 args:")
    print("- 1 arg: base folder")
    print("- 2 args: base folder, evec index (for color)")
    print("- 3 args: base folder, evec1 index, evec2")
    print("- 4 args: base folder, evec1 index, evec2 index, evec3 index")
else:
    # Get file names
    baseFolder = args[1]
    # Ensure that there is a slash in file path
    if baseFolder[-1] != os.sep:
        baseFolder += os.sep
    pointsFile = baseFolder + POINTS_FILENAME
    evecsFile = baseFolder + EVECS_FILENAME

    # Set up dict of evecs
    evecs = {}
    for i in range(2, numArgs+1):
        evecs[int(args[i])] = []
    if len(evecs) > 0:
        readColsFromFile(evecsFile, evecs)

    if numArgs in [1, 2]:

        # Read in points
        points = {}
        points[0] = []
        points[1] = []
        readColsFromFile(pointsFile, points)

        # Calculate color
        color = None
        if numArgs == 2:
            evecs = {}
            evecIndex = int(args[2])
            evecs[evecIndex] = []
            readColsFromFile(evecsFile, evecs)
            color = evecs[evecIndex]

        twoDimPlot(points[0], points[1], color=color)

    # Plot of 2 or 3 evecs
    else:
        evecs = {}
        for i in range(2, numArgs+1):
            evecs[int(args[i])] = []
        readColsFromFile(evecsFile, evecs)

        if numArgs == 3:
            [evecAIndex, evecBIndex] = list(evecs.keys())
            twoDimPlot(evecs[evecAIndex], evecs[evecBIndex], xLab=evecAIndex, yLab=evecBIndex)
        if numArgs == 4:
            threeDimPlot(evecs)
