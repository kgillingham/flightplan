# FlightPlanCalculator.py
# Last modified by Sarah Griffiths, 2-Dec-2020

print("This program will aid the designing process of an aerial photography remote sensing mission.") 
print("Specifically, this program will calculate the location, direction, and number of flight lines")
print("necessary to adequately photograph a given area, as well as the elevation the aircraft should fly at.")

# import math module for various trigonmetric functions
# import csv module to read and write csv files
import math
import csv



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


# Define input loop to get csv file and append to lists
def input_loop():

    ######## sarah: Add in the specifications how how the csv should be etc. etc. ######
    ####################################################################################

    cameratype = input("Will the camera be digital (D) or film (F)?: ")

    if cameratype.upper() == "F":
        # Create output csv file with all final outputs
        with open("FlightPlan-FilmOutput.csv", "a") as output_data:
            headerwriter = csv.writer(output_data)
            headerwriter.writerow([ ### all ouput headers here lol ###  ])

        # Following section by Sarah
        # Non-specific to camera type lists
        focallength = []         # create empty list for focallength
        elevation = []           # create empty list for elevation
        endlap = []              # create empty list for endlap
        sidelap = []             # create empty list for sidelap
        speed = []               # create empty list for speed
        cameratype = []  # if they are doing different project?? may be unneccessary. Could assume all would be D or F

        # Following section by Sarah
        # Lists for Film
        filmformatsizeinput = []    # create empty list for film format size input
        filmformatsize = []         # create empty list for calculated film format size  
        scaleinput = []             # create empty list for scale input
        scale = []                  # create empty list for calculated scale
        flyingheight = []           # create empty list for flying height
        singleimagegc = []          # create empty list for single image ground coverage
        groundphotosep = []         # create empty list for ground photo separation
        exposuretime = []           # create empty list for exposure time
        adjustedgroundphotosep = [] # create empty list for adjusted ground photo separation
        photosperline = []          # create empty list for number of photos per line
        distancebwlines = []        # create empty list for distance between lines
        flightlines = []            # create empty list for number of flight lines
        totalphotos = []            # create empty list for total photos
    elif cameratype.upper() == "D":
        # Create output csv file with all final outputs
        with open("FlightPlan-DigitalOutput.csv", "a") as output_data:
            headerwriter = csv.writer(output_data)
            headerwriter.writerow([ ### all ouput headers here lol ###  ])

        # Following section by Sarah
        # Non-specific to camera type lists
        focallength = []         # create empty list for focallength
        elevation = []           # create empty list for elevation
        endlap = []              # create empty list for endlap
        sidelap = []             # create empty list for sidelap
        speed = []               # create empty list for speed
        cameratype = []  # if they are doing different project?? may be unneccessary. Could assume all would be D or F
    
        # Following section by Sarah
        # Lists for Digital
        acrosstrack = []            # create empty list for across track ground coverage
        alongtrack = []             # create empty list for along track ground coverage
        pixelsize = []              # create empty list for pixel size 
        gsd = []                    # create empty list for ground sampling distance (?)
        flyingheight = []           # create empty list for flying height
        heightaboveterrain = []     # create empty list for height above the terrain
        acrosscoverage = []         # create empty list for across track coverage
        alongcoverage = []          # create empty list for along track coverage
        groundphotosep = []         # create empty list for ground photo separation
        exposuretime = []           # create empty list for exposure time
        photosperline = []          # create empty list for number of photos per line
        distancebwlines = []        # create empty list for distance between lines
        flightlines = []            # create empty list for number of light lines
        totalphotos = []            # create empty list for total photos



def calculation_loop():

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


    # Following section by Sarah
    # Get user inputs for values non-specific to camera type and store in unique variables
    focallength.append(float(input("In millimetres, what is the focal length of the camera? (e.g. 152.4): ")))
    print()
    print("For the purpose of this calculation, it is assumed that elevation will not vary over the desired study area.")
    elevation.append(int(input("In metres above sea level, what is the average terrain elevation above the datum? (e.g. 300): ")))
    print()
    endlap.append(float(input("As a percent, what is the desired amount of endlap? (e.g. 0.60): ")))
    print()
    sidelap.append(float(input("As a percent, what is the desired amount of sidelap? (e.g. 0.30): ")))
    print()
    speed = int(input("In kilometres/hour, what is the average ground speed of the aircraft? (e.g. 160): "))
    print()
    cameratype = input("Will the camera be digital (D) or film (F)?: ")
    

    #Selection case for camera type input
    #If input is Film camera
    if cameratype.upper() == "F":
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
    elif cameratype.upper() == "D":
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

    # call functions for calculations

    # print results on screen or in file??? if doing multiple entries from csv file, perhaps write to one?

def output_loop():

def main():
    input_loop()
    calculation_loop()
    output_loop()

if __name__ == "__main__":
    main()


