# This program will aid the designing process of an aerial photography remote sensing mission. 
# Specifically, this program will calculate the location, direction, and number of flight lines
# necessary to adequately photograph a given area, as well as the elevation the aircraft should fly at. 

# import math module for various trigonmetric functions
import math

def main():

    # radius of the Earth, in meters
    # this can be a global variable as it will not change
    radius = 6.3781e6

    coords = [[] for x in range(4)]

    # get 4 lat long pairs from the user, store in list
    coords[0].append(float(input("Point 1 latitude: ")))
    coords[0].append(float(input("Point 1 longitude: ")))
    coords[1].append(float(input("Point 2 latitude: ")))
    coords[1].append(float(input("Point 2 longitude: ")))
    coords[2].append(float(input("Point 3 latitude: ")))
    coords[2].append(float(input("Point 3 longitude: ")))
    coords[3].append(float(input("Point 4 latitude: ")))
    coords[3].append(float(input("Point 4 longitude: ")))

    # convert degrees to radians, store in list
    rcoords = [[] for x in range(4)]
    for x in range(len(coords)):
        for y in range(len(coords[0])):
            rcoords[x].append(math.radians(coords[x][y]))

    # pass radian values to haversine function
    distance = haversine(rcoords)


def haversine(coordinates):

    difflat1 = abs(coordinates[0][0] - coordinates[1][0])
    difflong1 = abs(coordinates[0][1] - coordinates[1][1])
    difflat2 = abs(coordinates[2][0] - coordinates[1][0])
    difflong2 = abs(coordinates[2][1] - coordinates[1][1])

    a1 = math.sin(difflat1/2)**2 + math.cos(coordinates[2][0]) * math.cos(coordinates[1][0]) * math.sin(difflong1/2)**2
    a2 = 2 * radius * math.atan2(math.sqrt(a1), math.sqrt(1 - a1))

    b1 = math.sin(difflat2/2)**2 + math.cos(coordinates[2][0]) * math.cos(coordinates[1][0]) * math.sin(difflong2/2)**2
    b2 = 2 * radius * math.atan2(math.sqrt(b1), math.sqrt(1 - b1))

    if a2 >= b2:
        length = a2
        width = b2
    else:
        length = b2
        width = a2
    
    return length, width

# This function assumes angles are in radians.
# Pass it the coordinates of the point furthest to the south west, or furthest to the west.
# Pass it the bearing of the long side of the rectangle in the direction of the 
# southern point to the northern point. If the points are on an E-W line, 
# 
def startingcoords(initCoords, numFlightLines, lineDistance, bearing):
    
    # angular distance
    distance = lineDistance / radius



if __name__ == "__main__":
    main()
