import sys
import numpy as np

# Input: np array
def standardizeCols (arr):
    arrMean = arr.sum(axis = 0) / len(arr)
    arrStd = arr.std(axis = 0)
    normalized = (arr - arrMean) / arrStd
    return normalized

# 2 args: input file, output file
args = sys.argv
if len(args) != 3:
    print("Enter 2 args: inputFile, outputFile")
else:
    inputFile = args[1]
    outputFile = args[2]
    notStandardized = np.loadtxt(inputFile, delimiter=",")
    standardized = standardizeCols(notStandardized)
    np.savetxt(outputFile, standardized, delimiter=",", fmt="%1.13f")
