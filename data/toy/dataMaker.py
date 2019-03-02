# Returns list of points
def makeTwoComponents ():

    points = []

    # First component
    for i in range(0,10):
        for j in range(0,10):
            points.append((i,j))

    # Second component
    for i in range(130, 140):
        for j in range(0,10):
            points.append((i,j))

    # Bridge
    for i in range(10, 130):
        points.append((i, 4))

    return points

def makeOneComponent ():
    points = []
    for i in range(2):
        for j in range(2):
            points.append((i,j))
    return points


def pointToString (point):
    ret = ""
    for i in range(len(point)):
        ret += str(point[i])
        if i != len(point) - 1:
            ret += ","
    return ret
# Mutates list
def pointsToStrings (points):
    for i in range(len(points)):
        points[i] = pointToString(points[i])

def writeLinesToFile (lines, filename):
    file = open(filename, 'w')
    for line in lines:
        file.write(line + "\n")
    file.close()

points = makeTwoComponents()
pointsToStrings(points)
writeLinesToFile(points, "twoComponents")
