# FlightPlanCalculator.py
# Last modified by Sarah Griffiths, 2-Dec-2020
# Calulates the flight plan of an aerial photography remote sensing mission
# calculates the location, direction, flying height, and number of flight lines 
# required to photograph an area
# Input in the form of a csv file and also keyboard input of camera type
# Outputs displayed on screen and in a CSV file

# import math module for various trigonmetric functions
# import csv module to read and write csv files
import math
import csv

###########################################  Start of inputs #################################################


################ Global variable lists to be accessed ##################
# Non-specific to camera type lists
focallength_list = []              # create empty list for focallength
elevation_list = []                # create empty list for elevation
endlap_list = []                   # create empty list for endlap
sidelap_list = []                  # create empty list for sidelap
speed_list = []                    # create empty list for speed
coords_list = [[] for x in range(4)]                        # create empty list to store pairs of coordinates

# Lists for Film
filmformatsizeinput_list = []      # create empty list for film format size input
scaleinput_list = []               # create empty list for scale input
# Lists for Digital
acrosstrack_list = []              # create empty list for across track ground coverage
alongtrack_list = []               # create empty list for along track ground coverage
pixelsize_list = []                # create empty list for pixel size 
gsd_list = []                      # create empty list for ground sampling distance (?)

# Define global variables 
radius = 6.3781e6
output_path = None            # Used to call output csv file in Loop

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


# Input loop if cameratype is Film
def Film_input_loop():
    print()
    # Ensure user has prepared csv correctly prior to import
    print("Prior to importing this program, please ensure your data has been entered following the requirements:")
    print("Film Format Size = mm (e.g. 230)")
    print("Desired Scale = denominator only (e.g. 25000)")
    print("Focal Length = mm (e.g. 152.4)")
    print("Average Terrain Elevation Above Datum = metres above sea level (e.g. 300)")
    print("Endlap  = percantage as decimal (e.g. 0.60)")
    print("Sidelap = percentage as decimal (e.g. 0.30)")
    print("Average Ground Speed of Plane = km/hr (e.g. 160)")
    print("The latitude and longitude of the 4 coordinates of the corner of the study area, starting with coordinate 1 latitude")
    print("You may also use the provided input csv template.")
    print()
    userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    print()
    # Thinking is hard today. Would while and break work for our loop instead of if/else? 
    # I can't think of how to get it to loop back up to get inputs while doing something with while
    # So long as the break stops it from doing it more than once?? I don't really remember how breaks work haha
    # while userready.upper() == "Y":
    if userready.upper() == "Y":
        input_path = str(input("Please enter the path to your input data csv file:  "))
        with open(input_path, "r") as input_data:
            input_read = csv.reader(input_data)
            header = next(input_read)
            for record in input_read:
                focallength_list.append(float(record[0]))
                elevation_list.append(float(record[1]))
                endlap_list.append(float(record[2]))
                sidelap_list.append(float(record[3]))
                speed_list.append(float(record[4]))
                filmformatsizeinput_list.append(float(record[5]))
                scaleinput_list.append(float(record[6]))
                coords_list[0].append(float(record[7]))
                coords_list[0].append(float(record[8]))
                coords_list[1].append(float(record[9]))
                coords_list[1].append(float(record[10]))
                coords_list[2].append(float(record[11]))
                coords_list[2].append(float(record[12]))
                coords_list[3].append(float(record[13]))
                coords_list[3].append(float(record[14]))
        # Call global csv variable and assign name depending on camera type
        output_location = str(input("What is the file path to the folder you want the output csv to be in?:   "))
        global output_path  
        output_path = open(output_location + "\\FlightPlan-FilmOutput.csv", "w")
        with open(output_path, "a") as output_data:
            headwriter = csv.writer(output_data)
            headwriter.writerow([ "Focal_Length(mm)", "Elevation_(meters_ASL)", "Endlap_(%)", "Sidelap_(%)", "Speed_(Km/h)", 
            "Film_Format_Size(mm)", "Scale_(1:  )","", "Flying_Height(meters_above_terrain)", "Flying_Height_Above_Sea_Level(m)" "",
            "Minimum_Flight_Lines", "Distance_Between_Lines(m)", "", "Total_Photos", "Photos_Per_Line"])
        # break
        # print("Please check your input data.")    
        # userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    else:
        print("Please confirm that you have checked your input data.")



def Digital_input_loop():  
    print()
    print("Across-Track Array Pixels = Total Pixels (e.g. 20010)")
    print("Along-track Array Pixels = Total Pixels (e.g. 13080")
    print("Physical Pixel Size = mm (e.g. 0.0052)")
    print("Ground Sampling Distance = m (e.g. 0.25)")       
    print("Focal Length = mm (e.g. 152.4)")
    print("Average Terrain Elevation Above Datum = metres above sea level (e.g. 300)")        
    print("Endlap = percantage as decimal (e.g. 0.60)")
    print("Sidelap = percentage as decimal (e.g. 0.30)")
    print("Average Ground Speed of Plane = km/hr (e.g. 160)")
    print()  
    userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    print()

    # Same issue as above. Delete whichever option is less effective
    # while userready.upper() == "Y":  
    if userready.upper() == "Y":
        input_path = str(input("Please enter the path to your input data csv file:  "))
        with open(input_path, "r") as input_data:
            input_read = csv.reader(input_data)
            header = next(input_read)
            for record in input_read:
                focallength_list.append(float(record[0]))
                elevation_list.append(float(record[1]))
                endlap_list.append(float(record[2]))
                sidelap_list.append(float(record[3]))
                speed_list.append(float(record[4]))
                acrosstrack_list.append(float(record[5]))
                alongtrack_list.append(float(record[6]))
                pixelsize_list.append(float(record[7]))
                gsd_list.append(float(record[8]))
        output_location = str(input("What is the file path to the folder you want the output csv to be in?:   "))
        global output_path 
        output_path = open(output_location + "\\FlightPlan-DigitalOutput.csv", "w")
        with open(output_path, "a") as output_data:
            headwriter = csv.writer(output_data)
            headwriter.writerow(["Focal_Length(mm)", "Elevation_(meters_ASL)", "Endlap_(%)", "Sidelap_(%)", "Speed_(Km/h)", 
            "Across_Track_Array", "Along_Track_Array", "Pixel_Size(mm)", "Ground_Sampling_Distance(m)", "", "Flying_Height(meters_above_terrain", 
            "Flying_Height_Above_Sea_Level(m)", "", "Minimum_Flight_Lines", "Distance_Between_Lines(m)", "", "Total_Photos", "Photos_Per_Line"])
    # break
    # print("Please check your input data.")    
    # userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    
    else:
        print("Please confirm that you have checked your input data.")


def Film_calcandoutput_loop():

    for index in range(len(focallength_list)):
        scaleinput = scaleinput_list[index]
        filmformatsizeinput = filmformatsizeinput_list[index]
        elevation = elevation_list[index]
        focallength = focallength_list[index]
        endlap = endlap_list[index]
        sidelap = sidelap_list[index]
        speed = speed_list[index]

        # convert degrees to radians, store in list
        rcoords = [[] for x in range(4)]
        
        for x in range(len(coords_list)):
            for y in range(len(coords_list[x])):
                rcoords[x].append(math.radians(coords_list[x][y]))

        # pass radian values to haversine function
        distance = haversine(rcoords)
        length = distance[0]
        width = distance[1]

        #Calcualte film camera specific variables
        scale = 1/scaleinput
        filmformatsize = filmformatsizeinput/1000
        flyingheight = (focallength/scale)+elevation
        heightaboveterrain = flyingheight - elevation
        singleimagegc = filmformatsize/scale
        groundphotosep = (1-endlap)*singleimagegc
        exposuretime = math.floor((groundphotosep/speed)*(3600/1000))
        adjustedgroundphotosep = exposuretime*speed*(1000/3600)
        photosperline = math.ceil((length/adjustedgroundphotosep)+1+1)
        distancebwlines = (1-sidelap)*singleimagegc
        flightlines = math.ceil((width/distancebwlines)+1)
        totalphotos = flightlines*photosperline

        #display final outputs for film camera
        print("Flying Height: ")
        print("With a camera focal length of ", focallength, " millimetres and a desired scale of 1:", scaleinput, 
        " at an average terrain elevation of ", elevation, " metres above sea level, flying height above terrain is ", heightaboveterrain, ". /n")
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

        # Create and
        with open(output_path, "a") as output_data:
            writer = csv.writer(output_data)
            writer.writerow([focallength, elevation, endlap, sidelap, speed, filmformatsizeinput, scaleinput, "", heightaboveterrain, flyingheight, 
            "", flightlines, distancebwlines, "", totalphotos, photosperline])    


def Digital_calcandouput_loop():

    for index in range(len(focallength_list)):
        focallength = focallength_list[index]
        elevation = elevation_list[index]
        endlap = endlap_list[index]
        sidelap = sidelap_list[index]
        speed = speed_list[index]
        acrosstrack = acrosstrack_list[index]
        alongtrack = alongtrack_list[index]
        pixelsize = pixelsize_list[index]
        gsd = gsd_list[index]

        # convert degrees to radians, store in list
        rcoords = [[] for x in range(4)]

        for x in range(len(coords_list)):
            for y in range(len(coords_list[x])):
                rcoords[x].append(math.radians(coords_list[x][y]))

        # pass radian values to haversine function
        distance = haversine(rcoords)
        length = distance[0]
        width = distance[1]

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
        " metres above sea level, flying height above terrain is ", heightaboveterrain, " metres. /n")
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

        with open(output_path, "a") as output_data:
            writer = csv.writer(output_data)
            writer.writerow([focallength, elevation, endlap, sidelap, speed, acrosstrack, alongtrack, pixelsize, gsd, "", heightaboveterrain, 
            flyingheight, "", flightlines, distancebwlines, "", totalphotos, photosperline])

    


def main():
    #try:
    
    # Indent following code once ready to use try:
    # Display Program Purpose
    print("This program will aid the designing process of an aerial photography remote sensing mission.") 
    print("Specifically, this program will calculate the location, direction, and number of flight lines")
    print("necessary to adequately photograph a given area, as well as the elevation at which the aircraft should fly.")
    print()
    print("For the purpose of this calculation, average terrain elevation and flying height of aircraft will not vary")
    print("over the desired study area.")
    print()
    # Get input for camera type
    cameratype = input("Will the camera be digital (D) or film (F)?: ")
    if cameratype.upper() == "F":
        Film_input_loop()
        Film_calcandoutput_loop()
        output_path.close()
    elif cameratype.upper() == "D":
        Digital_input_loop()
        Digital_calcandouput_loop()
        output_path.close()

    ## Error handling here ##
    # We can make these more specific. Just copied from Whale Mapping for now. Commented out so we can test code

    # Add exceptions to try condition for any errors that might occur
    # Display error as message
    # except TypeError as message:
    #     print(" There was an error: ", message)
    # except NameError as message:
    #     print(" There was an error: ", message)
    # except ValueError as message:
    #     print(" There was an error: ", message)
    # except SyntaxError as message: 
    #     print(" There was an error: ", message)
    # except RuntimeError as message:
    #     print(" There was an error: ", message)
    # except Exception as message:
    #     print(" There was an error: ", message)

if __name__ == "__main__":
    main()


