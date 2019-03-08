import sys
import os
import csv

args = sys.argv
numArgs = len(args) - 1
if numArgs < 3:
    print("Please follow this format:")
    print("<dataFile> <col1> <col2> (<col3>) (-color <colorFile>)")
    print("  example: points.csv 0 1")
    print("  example: points.csv 1 4 0 -color colors.csv")
else:
    dataFile = args[1]
    colorFile = None
    cols = []
    for i in range(2, len(args)):
        if args[i] == "-color":
            colorFile = args[i+1]
            break
        cols.append(int(args[i]))
