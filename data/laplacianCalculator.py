import sys
import os
import numpy as np
from numpy import linalg as la
import math

# Mutates list
def stringsToNumbers (list):
    for i in range(1,len(list)):
        list[i] = float(list[i])

# Return: list of points (each a list of coords)
def readPoints (filename):
    points = []
    file = open(filename, 'r')
    for line in file:
        coords = line.split(",")
        stringsToNumbers(coords)
        point = np.array(coords)
        points.append(point)
    return points

# Outputs value for gaussian dist
def pdf (x):
    return math.exp(-x*x/2.0) / math.sqrt(2.0*math.pi)
# Return: euclidian distance put through gaussian filter
def getDist (pointA, pointB):
    euclidDist = la.norm(pointA - pointB)
    dist = pdf(euclidDist)
    return dist

# Return:
# - symmetric matrix with cell (i,j) holding w(i,j)/degree(i)
# - list of sqrt(degree)
def getDistMatrixAndDegreeRoots (points):

    # Initialize dist matrix and degree array
    M = []
    degrees = []
    for i in range(len(points)):
        row = []
        for j in range(len(points)):
            row.append(0)
        M.append(row)
        degrees.append(0)

    # Consider all pairs of points
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = getDist(points[i], points[j])
            M[i][j] = -1 * dist
            M[j][i] = -1 * dist
            degrees[i] += dist
            degrees[j] += dist

    # Set diagonal to degrees
    for i in range(len(points)):
        M[i][i] = degrees[i]

    # Take the square root of all degrees
    degreeRoots = []
    for degree in degrees:
        degreeRoots.append(math.sqrt(degree))

    return np.array(M), degreeRoots

# Compute eigenvals and eigenvecs for a symmetric matrix
def getEigenValsAndVecs (symmetricM, putEvecsOnRows = False):
    evals, evecs = la.eigh(symmetricM)
    if putEvecsOnRows:
        evecs = np.transpose(evecs) # Put evecs on columns
    return evals, evecs

# Multiply evectors element-wise with degree roots to get final evectors
def adjustEvecs (evecs, degreeRoots):
    for i in range(len(evecs)):
        evecs[i] = np.multiply(evecs[i], degreeRoots[i])

# Convert list to comma-separated string
def pointToString (point):
    ret = ""
    for i in range(len(point)):
        ret += str(point[i])
        if i != len(point) - 1:
            ret += ","
    return ret

# File writing methods
def writeLinesToFile (lines, filename):
    file = open(filename, 'w')
    for line in lines:
        file.write(line + "\n")
    file.close()
def writeEvals (evals, evalFile):
    # Convert to strings
    strList = []
    for eval in evals:
        strList.append(str(eval))
    writeLinesToFile(strList, evalFile)
def writeEvecs (evecs, evecFile):
    # Convert to strings
    strList = []
    for evec in evecs:
        asStr = pointToString(evec)
        strList.append(asStr)
    writeLinesToFile(strList, evecFile)

# Input: data
# Output: evals (one per line), evecs (one per line)
def mainRoutine (inputFile, evalFile, evecFile):

    # Read input
    points = readPoints(inputFile)

    # Compute evals and evecs
    M, degreeRoots = getDistMatrixAndDegreeRoots(points)
    evals, evecs = getEigenValsAndVecs(M)
    adjustEvecs(evecs, degreeRoots) # Convert to final evecs for normalized matrix

    # Write output
    writeEvals(evals, evalFile)
    writeEvecs(evecs, evecFile)

args = sys.argv
numArgs = len(args)-1
if numArgs == 3:
    inputFile = args[1]
    evalFile = args[2]
    evecFile = args[3]
    mainRoutine(inputFile, evalFile, evecFile)
elif numArgs == 4:
    base = args[1]
    inputFile = base + os.sep + args[2]
    evalFile = base + os.sep + args[3]
    evecFile = base + os.sep + args[4]
    mainRoutine(inputFile, evalFile, evecFile)
elif numArgs == 2:
    base = args[1]
    inputFile = base + os.sep + args[2]
    evalFile = base + os.sep + "evals"
    evecFile = base + os.sep + "evecs.csv"
    mainRoutine(inputFile, evalFile, evecFile)
elif numArgs == 1:
    base = args[1]
    inputFile = base + os.sep + "points"
    evalFile = base + os.sep + "evals"
    evecFile = base + os.sep + "evecs.csv"
    mainRoutine(inputFile, evalFile, evecFile)
else:
    print("Must pass 1 to 4 args:")
    print("- 3 args: input file, evalue output file, evector output file")
    print("- 4 args: base folder + input, eval, evec")
    print("  - 2 args: base folder + input. Default output: evals, evecs.csv")
    print("  - 1 arg: base folder. Default input: points")
