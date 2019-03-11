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
DEFAULT_POINT_SIZE = 10;

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

def readColFromFile (fileName, colIndex):
    colsDict = {}
    colsDict[colIndex] = []
    readColsFromFile(fileName, colsDict)
    return colsDict[colIndex]

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

def twoDimPlot (x, y, xLab = None, yLab = None, color = None, pointSize = DEFAULT_POINT_SIZE):
    # Make plot
    marker = 'o'
    if color:
        plt.scatter(x, y, c=color, marker=marker, edgecolors='none', s=pointSize, cmap="gray")
    else:
        plt.scatter(x, y, marker=marker, edgecolors='none', s=pointSize, cmap="gray")

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
        ax.scatter(xyzDict[xi], xyzDict[yi], xyzDict[zi], c = color, edgecolors='none', s=pointSize, cmap="gray")
    else:
        ax.scatter(xyzDict[xi], xyzDict[yi], xyzDict[zi], edgecolors='none', s=pointSize, cmap="gray")

    ax.set_xlabel(xi)
    ax.set_ylabel(yi)
    ax.set_zlabel(zi)

    plt.show()

def printInstructions ():
    print("Please follow this format:")
    print("<dataFile> <col1> <col2> (<col3>) (-color <colorFile>)")
    print("  example: points.csv 0 1")
    print("  example: points.csv 1 4 0 -color colors.csv")

args = sys.argv
numArgs = len(args) - 1
if numArgs < 3:
    printInstructions()
else:
    evecsFile = args[1]
    colorFile = None
    colIndices = []
    for i in range(2, len(args)):
        if args[i] == "-color":
            i += 1
            colorFile = args[i]
            break
        colIndices.append(int(args[i]))

    # Set up dict of evecs
    evecs = {}
    for i in colIndices:
        evecs[i] = []
    if len(evecs) > 0:
        readColsFromFile(evecsFile, evecs)

    color = None
    if colorFile:
        color = readColFromFile(colorFile, 0)
        labelsToIndices(color)

    if len(evecs) == 2:
        [evecAIndex, evecBIndex] = list(evecs.keys())
        twoDimPlot(evecs[evecAIndex], evecs[evecBIndex], xLab=evecAIndex, yLab=evecBIndex, color=color)
    elif len(evecs) == 3:
        threeDimPlot(evecs, color=color)
    else:
        printInstructions()
