# Returns list of points
def makeTwoComponents ():

    points = []

    # Two components
    for i in range(0,10):
        for j in range(0,10):
            points.append((i,j))
            points.append((i+30,j))

    # Bridge
    for i in range(10, 30):
        points.append((i, 4))

    return points

def makeOneComponent ():
    points = []
    for i in range(2):
        for j in range(2):
            points.append((i,j))
    return points

def makeTriangle ():
    points = []
    for x in range(20):
        for y in range(x+1):
            points.append((x,y))
    return points

def makeFourComponents ():
    points = []
    for x in range(10):
        for y in range(10):
            points.append((x,y))
            points.append((x,y+30))
            points.append((x+110,y))
            points.append((x+110,y+30))
    for y in range(10,30):
        points.append((5,y))
        points.append((115,y))
    for x in range(5,115):
        points.append((x,20))
    return points

def makeTwoDisconnected ():
    points = []
    for x in range(10):
        for y in range(10):
            points.append((x,y))
            points.append((x+30,y))
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

points = makeTwoDisconnected()
pointsToStrings(points)
writeLinesToFile(points, "twoDisconnected/points")
