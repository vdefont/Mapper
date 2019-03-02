import sys
import numpy as np
from numpy import linalg as la
import math

# Mutates list
def stringsToNumbers (list):
    for i in range(len(list)):
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
    M = []
    degrees = []

    # Consider all pairs of points
    for i in range(len(points)):
        row = []
        for j in range(len(points)):
            if i == j:
                dist = 0
            else:
                dist = getDist(points[i], points[j])
            row.append(-1 * dist)
        # Calculate degree and scale down row
        M.append(row)
        degrees.append(-1 * np.sum(row))

    # Set diagonal to degrees
    for i in range(len(points)):
        M[i][i] = degrees[i]

    # Take the square root of all degrees
    degreeRoots = []
    for degree in degrees:
        degreeRoots.append(math.sqrt(degree))

    return np.array(M), degreeRoots

# Compute eigenvals and eigenvecs for a symmetric matrix
def getEigenValsAndVecs (symmetricM):
    evals, evecs = la.eigh(symmetricM)
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
if len(args) != 4:
    print("Give 3 args: input file, evalue output file, evector output file")
else:
    inputFile = args[1]
    evalFile = args[2]
    evecFile = args[3]
    mainRoutine(inputFile, evalFile, evecFile)
