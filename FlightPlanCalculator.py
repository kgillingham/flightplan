# This program will aid the designing process of an aerial photography remote sensing mission. 
# Specifically, this program will calculate the location, direction, and number of flight lines
# necessary to adequately photograph a given area, as well as the elevation the aircraft should fly at. 

# import math module for various trigonmetric functions
import math

>>>>>>> 3a986c59a157e5447ce2fd902c9b81b70511c668
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





#Selection case for camera type input
#If input is Film camera
if cameratype == "F":
    #Get inputs for film camera specific variahbles
    filmformatsizeinput = float(input("In millimetres, what is the film format size? (e.g. 230): "))
    filmformatsize = filmformatsizeinput/1000
    scaleinput = float(input("What is the desired scale? Please enter the denominator only (e.g. 25000). Scale = 1: "))
    scale = 1/scaleinput
    #Calcualte film camera specific variables
    flyingheight = (focallength/scale)+elevation
    singleimagegc = filmformatsize/scale
    groundphotosep = (1-endlap)*singleimagegc
    exposuretime = math.floor((groundphotosep/speed)*(3600/1000))
    adjustedgroundphotosep = exposuretime*speed*(1000/3600)
    photosperline = math.ciel((length/adjustedgroundphotosep)+1+1)
    distancebwlines = (1-sidelap)*singleimagegc
    flightlines = math.ceil((width/distancebwlines)+1)
    totalphotos = flightlines*photosperline
    #display final outputs for film camera
    print("Flying Height: ")
    print("With a camera focal length of ", focallength, " millimetres and a desired scale of 1:", scaleinput, 
    " at an average terrain elevation of ", elevation, " metres above sea level, flying height above terrain is ", flyingheight, ". /n")
    print("Minimum Flight Lines: ")
    print("With a film format size of ", filmformatsizeinput, " millimetres and scale of 1:", scaleinput, 
    ", the ground cover of a single image is ", singleimagegc, "metres on a side")
    print("With a desired sidelap of ", (sidelap*100), "%, there should be ", distancebwlines, " metres between flight lines.")
    print("With the study area wdith of ", width, " metres, the minimum number of flight lines is ", flightlines, ". /n")
    print("Minimum Numbers of Photographs: ")
    print("With a desired endlap of ", (endlap*100), "%, ground photo seperation is ", groundphotosep, " metres.")
    print("With an aircraft speed of ", speed, "km/h, time between exposures is ", exposuretime, " seconds.")
    print("With an adjusted distance of ", adjustedgroundphotosep, " metres between photographs, the minimum number of photos per line is ", 
    photosperline, ". /n")
    print("The total number of photographs taken will be ", totalphotos, ".")


#Selection case for camera type input
#If input is digital camera
elif cameratype == "D":
    #Get inputs for digital camera specific variables
    acrosstrack = float(input("What is the number of pixels in the across-track sensor array? (e.g. 20010): "))
    alongtrack = float(input("What is the number of pixels in the along-track sensor array? (e.g. 13080): "))
    pixelsize = float(input("In millimetres, whaty is the physical size of each pixel? (e.g. 0.0052): "))
    gsd =  float(input("In metres, what is the ground smapling distance? (e.g. 0.25): ")
    #Calcualte digital camera specific variables
    flyingheight = ((gsd*focallength)/pixelsize)+elevation
    heightaboveterrain = flyingheight-elevation 
    acrosscoverage = ((acrosstrack*pixelsize)*heightaboveterrain)/focallength
    alongcoverage = ((alongtrack*pixelsize)*heightaboveterrain)/focallength
    groundphotosep = (1-endlap)*alongcoverage
    exposuretime = math.floor((groundphotosep/speed)*(3600/1000))
    photosperline = math.ceil((length/groundphotosep)+1+1)
    distancebwlines = (1-sidelap)*acrosscoverage
    flightlines = math.ceil((width/distancebwlines)+1)
    totalphotos = flightlines*photosperline
    #Display final outputs for digital camera
    print("Flying Height: ")
    print("With a focal length of ", focallength, " millimetres, a pixel size of ", pixelsize, 
    " millimetres, a ground sampling distance of ", gsd, " metres, and at an average terrain elevation of ", elevation, 
    " metres above sea level, flying height above terrain is ", flyingheight, " metres. /n")
    print("Minimum Flight Lines: ")
    print("Across track ground coverage distance with ", acrosstrack, " pixels is ", acrosscoverage, " metres.")
    print("With a desired sidelap of ", sidelap, "%, there should be ", distancebwlines, " metres between flight lines.")
    print("With a study area width of ", width, " metres, the minimum number of flight lines is ", flightlines, ". /n")
    print("Minimum Number of Photographs: ")
    print("Along track ground coverage distance with ", alongtrack, " pixels is ", alongcoverage, " metres.")
    print("With a desired endlap of ", endlap, " %, ground photo seperation is ", groundphotosep, " metres.")
    print("With an aircraft speed of ", speed, "km/h, time between exposures is ", exposuretime, " seconds.")
    print("With a distance of ", groundphotosep, " metres between photographs, the minimum number of photos per line is ", photosperline, ". /n")
    print("The total number of photographs taken will be ", totalphotos, ".")



else:
    Print("Please check your input. Enter 'F' for film camera and 'D' for digital camera")



