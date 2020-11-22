# This program will aid the designing process of an aerial photography remote sensing mission. 
# Specifically, this program will calculate the location, direction, and number of flight lines
# necessary to adequately photograph a given area, as well as the elevation the aircraft should fly at. 

# import math module for the radians function
import math

def main():

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

    print(len(coords), len(coords[0]))

    # convert degrees to radians
    rcoords = [[] for x in range(4)]
    for x in range(len(coords)):
        for y in range(len(coords[0])):
            rcoords[x].append(math.radians(coords[x][y]))

    # pass radian values to haversine function
    haversine(rcoords)

# TO DO
def haversine(coordinates):

    print('test')

if __name__ == "__main__":
    main()
