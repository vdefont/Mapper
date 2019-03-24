import sys
import os
import numpy as np
from numpy import linalg as la
import math
import random
import heapq

import util

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
def extendSampleToAll (pointsAll, sampledIndices, evecsSampled, kNearest):

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
            # Build queue of nearest items
            queue = []
            for j in range(len(sampledIndices)):
                sampledIndex = sampledIndices[j]
                dist = getDist(pointsAll[i], pointsAll[sampledIndex])
                val = evecsSampled[j]
                heapq.heappush(queue, (dist, val))
            # Get k nearest
            sum = []
            for i in range(len(evecsSampled[0])):
                sum.append(0.0)
            for i in range(kNearest):
                _, val = heapq.heappop(queue)
                for j in range(len(sum)):
                    sum[j] += val[j]
            for i in range(len(sum)):
                sum[i] /= kNearest

            evecs.append(sum)

    return np.array(evecs)


# Input: data
# Output: evals (one per line), evecs (one per line)
def mainRoutine (inputFile, evalFile, evecFile, sampleFraction, kNearest):

    # Read input
    pointsAll = np.loadtxt(inputFile, delimiter=",")
    points, sampledIndices = samplePoints(pointsAll, sampleFraction)

    # Compute evals and evecs
    distM, degreeRoots = getDistMatrixAndDegreeRoots(points)
    evals, evecs = getEigenValsAndVecs(distM)
    adjustEvecs(evecs, degreeRoots) # Convert to final evecs for normalized matrix

    # Extend to include all points not sampled
    if sampleFraction:
        evecs = extendSampleToAll(pointsAll, sampledIndices, evecs, kNearest)

    # Write output
    np.savetxt(evalFile, evals, delimiter=",", fmt="%1.13f")
    np.savetxt(evecFile, evecs, delimiter=",", fmt="%1.13f")


def printInstructions():
    print("Invalid args. Please use:")
    print("-inputFile <file>")
    print("-evalFile <file>")
    print("-evecFile <file>")
    print("Optional:")
    print("-sampleFraction <0.2> (used for landmarking)")
    print("-kNeareast <2> (used for landmarking. Default 1)")

requiredArgs = ["inputFile", "evalFile", "evecFile"]
args = util.parseArgs(sys.argv, requiredArgs = requiredArgs)
if not args:
    printInstructions()
else:
    inputFile = args["inputFile"][0]
    evalFile = args["evalFile"][0]
    evecFile = args["evecFile"][0]

    sampleFraction = None
    if "sampleFraction" in args:
        sampleFraction = float(args["sampleFraction"][0])

    kNearest = 1
    if "kNearest" in args:
        kNearest = int(args["kNearest"][0])

    mainRoutine(inputFile, evalFile, evecFile, sampleFraction, kNearest)
