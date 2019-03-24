import csv

# Parse args, return a dict of the args
def parseArgs(args, firstArg = "", requiredArgs = []):
    argsDict = {}
    curTitle = firstArg
    cur = []
    for i in range(1, len(args)):
        arg = args[i]
        if arg[0] == '-':
            if len(cur) > 0:
                argsDict[curTitle] = cur
            curTitle = arg[1:]
            cur = []
        else:
            cur.append(arg)
    # Store last arg
    if len(cur) > 0:
        argsDict[curTitle] = cur

    # Ensure all required args are present
    for arg in requiredArgs:
        if arg not in argsDict:
            return False

    return argsDict

# Returns dict: index -> vals
def readColsFromFile (fileName, colIndices):

    colsDict = {}
    for i in colIndices:
        colsDict[i] = []

    # Read from file to populate dict
    with open(fileName, 'r') as csvFile:
        # Read each row
        rows = csv.reader(csvFile, delimiter=',')
        for row in rows:
            for colIndex in colsDict:
                colsDict[colIndex].append(float(row[colIndex]))
    return colsDict
# Reads single column from file
def readColFromFile (fileName, colIndex):
    colsDict = readColsFromFile(fileName, [colIndex])
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

# Mutates array to make all elements integers
def toIntArray(arr):
    for i in range(len(arr)):
        arr[i] = int(arr[i])
