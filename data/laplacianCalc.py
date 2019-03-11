import sys
import os
import numpy as np
from numpy import linalg as la
import math
import random

###############
# Input file does not need to have normalized columns

# Outputs value for gaussian dist
def pdf (x):
    return math.exp(-x*x/2.0) / math.sqrt(2.0*math.pi)
# Return: euclidian distance put through gaussian filter
def getDist (pointA, pointB, gaussianFilter = False):
    sum = 0.0
    for i in range(len(pointA)):
        sum += (float(pointA[i]) - float(pointB[i])) ** 2
    dist = math.sqrt(sum)
    if gaussianFilter:
        dist = pdf(dist)
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
            dist = getDist(points[i], points[j], gaussianFilter = True)
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
def getEigenValsAndVecs (distM):
    evals, evecs = la.eigh(distM)
    return evals, evecs

# Multiply evectors element-wise with degree roots to get final evectors
def adjustEvecs (evecs, degreeRoots):
    for i in range(len(evecs)):
        evecs[i] = np.multiply(evecs[i], degreeRoots[i])

# Returns (sampled points, sampledIndices)
def samplePoints (points, sampleFrac):
    numRows = len(points)
    if sampleFrac is None:
        return points, range(numRows)
    else:
        numToSample = int(sampleFrac * numRows)
        sampleIndices = random.sample(range(numRows), numToSample)
        list.sort(sampleIndices)
        return points[sampleIndices,:], sampleIndices

# Returns evecs, extended to all points
def extendSampleToAll (pointsAll, sampledIndices, evecsSampled):

    evecsSampled = evecsSampled.tolist()

    # Populate list with every point
    evecs = []
    indexInSmallList = 0
    for i in range(len(pointsAll)):

        if i in sampledIndices:
            evecs.append(evecsSampled[indexInSmallList])
            indexInSmallList += 1

        # If not sampled, find closest sample
        else:
            bestDist = None
            closestIndex = None
            for j in range(len(sampledIndices)):
                sampledIndex = sampledIndices[j]
                curDist = getDist(pointsAll[i], pointsAll[sampledIndex])
                if bestDist is None or curDist < bestDist:
                    bestDist = curDist
                    closestIndex = j
            evecs.append(evecsSampled[closestIndex])

    return np.array(evecs)


# Input: data
# Output: evals (one per line), evecs (one per line)
def mainRoutine (inputFile, evalFile, evecFile, sampleFraction):

    # Read input
    pointsAll = np.loadtxt(inputFile, delimiter=",")
    points, sampledIndices = samplePoints(pointsAll, sampleFraction)

    # Compute evals and evecs
    distM, degreeRoots = getDistMatrixAndDegreeRoots(points)
    evals, evecs = getEigenValsAndVecs(distM)
    adjustEvecs(evecs, degreeRoots) # Convert to final evecs for normalized matrix

    # Extend to include all points not sampled
    if sampleFraction:
        evecs = extendSampleToAll(pointsAll, sampledIndices, evecs)

    # Write output
    np.savetxt(evalFile, evals, delimiter=",", fmt="%1.13f")
    np.savetxt(evecFile, evecs, delimiter=",", fmt="%1.13f")

args = sys.argv
numArgs = len(args)-1

# Handle -sampleFraction flag
sampleFraction = None
if numArgs >= 2 and args[-2] == "-sampleFraction":
    sampleFraction = float(args[-1])
    numArgs -= 2

# Handle rest of data
if numArgs == 3:
    inputFile = args[1]
    evalFile = args[2]
    evecFile = args[3]
    mainRoutine(inputFile, evalFile, evecFile, sampleFraction)
elif numArgs == 4:
    base = args[1]
    inputFile = base + os.sep + args[2]
    evalFile = base + os.sep + args[3]
    evecFile = base + os.sep + args[4]
    mainRoutine(inputFile, evalFile, evecFile, sampleFraction)
elif numArgs == 2:
    base = args[1]
    inputFile = base + os.sep + args[2]
    evalFile = base + os.sep + "evals"
    evecFile = base + os.sep + "evecs.csv"
    mainRoutine(inputFile, evalFile, evecFile, sampleFraction)
elif numArgs == 1:
    base = args[1]
    inputFile = base + os.sep + "points.csv"
    evalFile = base + os.sep + "evals"
    evecFile = base + os.sep + "evecs.csv"
    mainRoutine(inputFile, evalFile, evecFile, sampleFraction)
else:
    print("Must pass 1 to 4 args:")
    print("- 3 args: input file, evalue output file, evector output file")
    print("- 4 args: base folder + input, eval, evec")
    print("  - 2 args: base folder + input. Default output: evals, evecs.csv")
    print("  - 1 arg: base folder. Default input: points.csv")
    print("Optional: -sampleFraction flag at the end")
