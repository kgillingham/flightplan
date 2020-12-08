import math

radius = 6.3781e6

# function calculates the distance and bearing between points 1, 2, and 3 of the rectangle. 
# The points MUST be inputted so that each successive point is adjacent to the last; i.e. point pairs 1/2, 2/3, or 3/4 cannot be on opposite sides of the rectangle
def haversine(coordinates):

    difflat1 = abs(coordinates[0][0] - coordinates[1][0])
    difflong1 = coordinates[1][1] - coordinates[0][1]
    difflat2 = abs(coordinates[2][0] - coordinates[1][0])
    difflong2 = coordinates[2][1] - coordinates[1][1]

    # calculate the distance and bearing between points 1 and 2 of the rectangle. The bearing is in the direction of 1 to 2
    a1 = math.sin(difflat1/2)**2 + math.cos(coordinates[0][0]) * math.cos(coordinates[1][0]) * math.sin(difflong1/2)**2
    a2 = 2 * radius * math.atan2(math.sqrt(a1), math.sqrt(1 - a1))
    aBearing = math.atan2(math.sin(difflong1) * math.cos(coordinates[1][0]), math.cos(coordinates[0][0]) * math.sin(coordinates[1][0]) - math.sin(coordinates[0][0]) * math.cos(coordinates[1][0]) * math.cos(difflong1))

    # calculate the distance and bearing between points 2 and 3 of the rectangle. The bearing is in the direction of 2 to 3
    b1 = math.sin(difflat2/2)**2 + math.cos(coordinates[2][0]) * math.cos(coordinates[1][0]) * math.sin(difflong2/2)**2
    b2 = 2 * radius * math.atan2(math.sqrt(b1), math.sqrt(1 - b1))
    bBearing = math.atan2(math.sin(difflong2) * math.cos(coordinates[2][0]), math.cos(coordinates[1][0]) * math.sin(coordinates[2][0]) - math.sin(coordinates[1][0]) * math.cos(coordinates[2][0]) * math.cos(difflong2))

    # Whichever side of the rectangle is longer will be the direction the flight lines will be in.
    # The variable oneToTwo will help the startingCoords function determine which corner point to add distance from, to get the starting coordinates of each of the flight lines.
    # If oneToTwo is True, this means that the long side of the rectangle is along the line between points 1 and 2 (point 1 is the first coordinate inputted by the user, point 2 is the second, etc).
    # In this case shortBearing is the bearing from point 2 to point 3, which is the bearing that distance will be measured along starting at point 2, which will result in the starting coordinates
    # of the flight lines. Am I making any sense?????? 

    if a2 >= b2:
        length = a2
        width = b2
        longBearing = aBearing
        shortBearing = bBearing
        oneToTwo = True
    else:
        length = b2
        width = a2
        longBearing = bBearing
        shortBearing = aBearing
        oneToTwo = False
    
    return length, width, longBearing, shortBearing, oneToTwo



def destinationPoint(startingPoint, direction, angularDistance):
    nextCoordinates = []
    nextCoordinates.append(math.asin(math.sin(startingPoint[0]) * math.cos(angularDistance) + math.cos(startingPoint[0]) * math.sin(angularDistance) * math.cos(direction)))
    nextCoordinates.append(startingPoint[1] + math.atan2(math.sin(direction) * math.sin(angularDistance) * math.cos(startingPoint[0]), math.cos(angularDistance) - math.sin(startingPoint[0]) * math.sin(nextCoordinates[0])))
    return nextCoordinates



# This function assumes angles are in radians.
# Pass it the list of coordinates, the bearing of the long side of the rectangle, and the number of flight lines required
def startingCoords(initCoords, lineDistance, numFlightLines):

    # get the bearing of the short side of the rectangle from the haversine function
    haversineResult = haversine(initCoords)
    
    # the bearing of the long (index 2) and short (index 3) sides are stored in separate variables
    bearingLong = haversineResult[2]
    bearingShort = haversineResult[3]

    # this variable stores the opposite bearing of bearingLong, i.e. 180 degrees apart
    bearingLongOpposite = (bearingLong + math.pi) % (2 * math.pi)

    # angular distance between flight lines
    angularDistShort = lineDistance / radius

    # angular distance of the long side of the rectangle
    angularDistLong = haversineResult[0] / radius

    # if oneToTwo (index 4 of haversineResult) is true, then measure distance starting at point 2 towards point 3. If it is false, then use points 1 to 2.
    if haversineResult[4]:
        start = initCoords[1]
    else:
        start = initCoords[0]

    # declare list that will store the list of starting coordinates. The number of starting coordinates that will need to be calculated is the number of flight lines - 1
    startingCoordinates = []
    startingCoordinates.append(start)

    
    # This whole chunk of code is hard to explain without a diagram but I will try. 
    # Adjacent flight lines must start at opposite ends of the rectangle, as that will be the direction that the plane will be coming from after flying across it in one direction.
    # In order to calculate the starting coordinates of the next flight line, first an intermediate point must be calculated which is on the opposite side of the rectangle, 
    # on a line parallel to the long side of the rectangle from the previous point. From here, the actual next starting point can be calculated.
    # If the iterator x is an even number then the opposite of the long bearing must be used.
    for x in range(numFlightLines - 1):
        # if x == 0:
        #     destination = destinationPoint(start, bearingShort, angularDistShort)
        #     start = destination

        if x % 2 != 0:
            intermediatePoint = destinationPoint(start, bearingLong, angularDistLong)
        else:
            intermediatePoint = destinationPoint(start, bearingLongOpposite, angularDistLong)

        destination = destinationPoint(intermediatePoint, bearingShort, angularDistShort)

        startingCoordinates.append(destination)
        start = destination

    degCoords = [[] for x in range(numFlightLines)]
    for x in range(len(startingCoordinates)):
        for y in range(len(startingCoordinates[x])):
            degCoords[x].append(math.degrees(startingCoordinates[x][y]))

    print(degCoords)
    return(degCoords)



def main():
    coords = [[45.5236, -75.6009], [45.3236, -75.6009], [45.3236, -75.7509], [45.5236, -75.7509]]

    rcoords = [[] for x in range(4)]
    for x in range(len(coords)):
        for y in range(len(coords[x])):
            rcoords[x].append(math.radians(coords[x][y]))


    rStart = startingCoords(rcoords, 3910, 4)

    print(rStart)

main()