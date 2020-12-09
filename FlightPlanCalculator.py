# FlightPlanCalculator.py
# Last modified 9-Dec-2020
# Authors - Kazuto Gillingham, Lucy Lin, Sarah Griffiths


# Program Purpose and Use:
# Calulates the flight plan of an aerial photography remote sensing mission
# calculates the location, direction, flying height, and number of flight lines 
# required to photograph an area
# Input in the form of a csv file and also keyboard input of camera type
# Outputs displayed on screen and in a CSV file

# Program Summary:

# Assumptions Affecting Program Strcture:
# It is assumed that terrain elevation does not change over the study area (we use "Average Terrain Elevation")
# It is assumed that the flying height of the aircraft stays constant over the study area.
# It is only possible to input a csv with one record whereas in flight planning, multiple flights would be planned at once.

# Special Cases and Known Problems:
# During data validation, if the inputs are not suitable, the program ends. 
# This causes an issue if the FlightPlan-(CameraType)Output.csv is not deleted before the program is run again as
# the program will write a second row of headers, followed by the data inputs and calculations.

# Inputs:
# Camera Type (Digital/Film)
# Focal Length
# Average Terrain Elevation
# Desired Endlap
# Desired Sidelap
# Aircraft Speed
# Four Pairs of Coordinates representing the 4 corners of study area
# Film Format (Film Only)
# Scale (Film Only)
# Across Track Array Pixel Amount (Digital Only)
# Along Track Array Pixel Amount (Digital Only)
# Physical Pixel Size (Digital Only)
# Ground Sampling Distance (Digital Only)

# Outputs:
# Flying Height Above Terrain
# Flying Height Above Sea Level
# Miniumum Number of Flight Lines
# Distance Between Flight Lines
# Total Number of Photos
# Total Number of Photos Per Line
# Starting Coordinates of Each Flight Line


# Citations and Resources:
# Lillesand, T.M., Kiefer, R.W., Chipman, J.W. (2018). Remote Sensing And Image Interpretation – Seventh Edition. Wiley.

# Division of Work: 
# Kazuto - haversine, destinationPoint, and startingCoords functions
# Lucy - input loops, calcandoutput loops, csv input and output
# Sarah - User verification that csv data in appropriate ranges/units. Data Validation. Error Handling. Creation of empty lists for variables


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
coords_list = [[] for x in range(4)]       # create empty list to store pairs of coordinates

# Lists for Film
filmformatsizeinput_list = []      # create empty list for film format size input
scaleinput_list = []               # create empty list for scale input
# Lists for Digital
acrosstrack_list = []              # create empty list for across track ground coverage
alongtrack_list = []               # create empty list for along track ground coverage
pixelsize_list = []                # create empty list for pixel size 
gsd_list = []                      # create empty list for ground sampling distance (?)

# Define global variables 
radius = 6.3781e6                  # assign radius as a global variable as it will be used throughout the program
# Ouput_path is a global variable because we want to assign the path and file name depending on the camera type within the main function
# We did not want to have to return the output_path each loop to be used in the next. This is more efficient
output_path = None                 # Used to call output csv file in Loop




# Function calculates the distance and bearing between points 1 to 2, and 2 to 3 of the rectangle. 
# The points MUST be inputted so that each successive point is adjacent to the last; i.e. point pairs 1/2, 2/3, or 3/4 cannot be on opposite sides of the rectangle
# Coordinates passed to this function must be in radians.
def haversine(coordinates):
    # Calculate difference in lat/longs of the point pairs 1/2 and 2/3
    difflat1 = abs(coordinates[0][0] - coordinates[1][0])
    difflong1 = coordinates[1][1] - coordinates[0][1]
    difflat2 = abs(coordinates[2][0] - coordinates[1][0])
    difflong2 = coordinates[2][1] - coordinates[1][1]

    # Calculate the distance and bearing between points 1 and 2 of the rectangle. The bearing is in the direction of 1 to 2.
    a1 = math.sin(difflat1/2)**2 + math.cos(coordinates[0][0]) * math.cos(coordinates[1][0]) * math.sin(difflong1/2)**2
    a2 = 2 * radius * math.atan2(math.sqrt(a1), math.sqrt(1 - a1))
    aBearing = math.atan2(math.sin(difflong1) * math.cos(coordinates[1][0]), math.cos(coordinates[0][0]) * math.sin(coordinates[1][0]) - math.sin(coordinates[0][0]) * math.cos(coordinates[1][0]) * math.cos(difflong1))

    # Calculate the distance and bearing between points 2 and 3 of the rectangle. The bearing is in the direction of 2 to 3.
    b1 = math.sin(difflat2/2)**2 + math.cos(coordinates[2][0]) * math.cos(coordinates[1][0]) * math.sin(difflong2/2)**2
    b2 = 2 * radius * math.atan2(math.sqrt(b1), math.sqrt(1 - b1))
    bBearing = math.atan2(math.sin(difflong2) * math.cos(coordinates[2][0]), math.cos(coordinates[1][0]) * math.sin(coordinates[2][0]) - math.sin(coordinates[1][0]) * math.cos(coordinates[2][0]) * math.cos(difflong2))

    # Whichever side of the rectangle is longer will be the direction the flight lines will be in.
    # The variable oneToTwo will help the startingCoords function determine which corner point to add distance from, to get the starting coordinates of each of the flight lines.
    # If oneToTwo is True, this means that the long side of the rectangle is along the line between points 1 and 2 (point 1 is the first coordinate inputted by the user, point 2 is the second, etc).
    # In this case shortBearing is the bearing from point 2 to point 3, which is the bearing that distance will be measured to calculate the starting coordinates of the flight lines.

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
    
    # function returns the length and width of the rectangle, the bearings of the long and short sides, and a boolean value containing whether or not the line between
    # points 1 and 2 is the long side. Angles will be in radians
    return length, width, longBearing, shortBearing, oneToTwo


# Function receives 3 parameters (coordinates of the starting point, the bearing to add distance in, and the angular distance).
def destinationPoint(startingPoint, direction, angularDistance):
    nextCoordinates = []
    # Calculate the lat of the destination point
    nextCoordinates.append(math.asin(math.sin(startingPoint[0]) * math.cos(angularDistance) + math.cos(startingPoint[0]) * math.sin(angularDistance) * math.cos(direction)))
    # Calculate the long of the destination point
    nextCoordinates.append(startingPoint[1] + math.atan2(math.sin(direction) * math.sin(angularDistance) * math.cos(startingPoint[0]), math.cos(angularDistance) - math.sin(startingPoint[0]) * math.sin(nextCoordinates[0])))
    # Returns one pair of lat long coordinates in radians.
    return nextCoordinates



# This function assumes angles are in radians.
# Pass it the list of coordinates, the distance between flight lines, and the number of flight lines required.
def startingCoords(initCoords, lineDistance, numFlightLines):

    # Call the haversine function.
    haversineResult = haversine(initCoords)
    
    # The bearing of the long (index 2) and short (index 3) sides are stored in separate variables.
    bearingLong = haversineResult[2]
    bearingShort = haversineResult[3]

    # This variable stores the opposite bearing of bearingLong, i.e. 180 degrees apart.
    bearingLongOpposite = (bearingLong + math.pi) % (2 * math.pi)

    # Angular distance between flight lines.
    angularDistShort = lineDistance / radius

    # Angular distance of the long side of the rectangle.
    angularDistLong = haversineResult[0] / radius

    # If oneToTwo (index 4 of haversineResult) is true, then measure flight lines starting at point 2 towards point 3. If it is false, then start at point 1 and go towards 2.
    if haversineResult[4]:
        start = initCoords[1]
    else:
        start = initCoords[0]

    # Declare list that will store the list of starting coordinates. The number of starting coordinates that will need to be calculated is the number of flight lines - 1.
    startingCoordinates = []
    # Append the coordinates of the corner of the rectangle, which will be the start location of the first flight line.
    startingCoordinates.append(start)

    
    # This next chunk of code is hard to explain without a diagram but I will try. 
    # Adjacent flight lines must start at opposite ends of the rectangle, as that will be the direction that the plane will be coming from after flying across it in one direction.
    # In order to calculate the starting coordinates of the next flight line, first an intermediate point must be calculated which is on the opposite side of the rectangle, 
    # on the line parallel to the long side of the rectangle starting from the previous point. From this intermediate point, the next starting point can be calculated 
    # by adding the distance between flight lines in the short bearing direction.
    # If the iterator x is an even number then the opposite of the long bearing must be used.
    for x in range(numFlightLines - 1):
        if x % 2 != 0:
            intermediatePoint = destinationPoint(start, bearingLong, angularDistLong)
        else:
            intermediatePoint = destinationPoint(start, bearingLongOpposite, angularDistLong)

        destination = destinationPoint(intermediatePoint, bearingShort, angularDistShort)
        startingCoordinates.append(destination)
        start = destination

    # Convert radians back to degrees.
    degCoords = [[] for x in range(numFlightLines)]
    for x in range(len(startingCoordinates)):
        for y in range(len(startingCoordinates[x])):
            degCoords[x].append(math.degrees(startingCoordinates[x][y]))

    return(degCoords)
    


# Input loop if cameratype is Film
def Film_input_loop():
    print()
    # Ensure user has prepared csv correctly prior to import, primarly concerning units of measure
    # This is done as an outside "data validation" to double check that the user understands what is required to run the program
    # Having the user verify the data before import prevents the need to start program over and delete csv created before validation    
    print("Prior to importing this program, please ensure your data has been entered following the requirements:")
    print("Focal Length = mm (e.g. 152.4)")
    print("Average Terrain Elevation Above Datum = metres above sea level (e.g. 300)")
    print("Endlap  = percantage as decimal (e.g. 0.60)")
    print("Sidelap = percentage as decimal (e.g. 0.30)")
    print("Average Ground Speed of Plane = km/hr (e.g. 160)")
    print("Film Format Size = mm (e.g. 230)")
    print("Desired Scale = denominator only (e.g. 25000)")   
    print("The latitude and longitude of the 4 coordinates of the corner of the study area, starting with coordinate 1 latitude")
    print("You may also use the provided input csv template.")
    print()
    userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    print()
    # If user enters Y/y the program will proceed to read the input from their csv, otherwise it will end
    # Program ends instead of loops because the process of checking the data could be lengthy
    if userready.upper() == "Y":
        # prompt input for file path of desired csv file
        input_path = str(input("Please enter the path to your input data csv file:  "))
        # open and read csv file and append values to global lists 
        with open(input_path, "r") as input_data:
            input_read = csv.reader(input_data)
            # Skips over first record, which are the headers 
            next(input_read)
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
        # prompt input of output csv location path
        output_location = str(input("What is the file path to the folder you want the output csv to be in?:   "))
        # Call global csv variable and assign name depending on camera type
        global output_path  
        # Name output csv file according to camera type selected
        output_path = output_location + "FlightPlan-FilmOutput.csv"
        # Open output csv file and append a header row with header
        with open(output_path, "a") as output_data:
            headwriter = csv.writer(output_data)
            headwriter.writerow([ "Focal_Length(mm)", "Elevation_(meters_ASL)", "Endlap_(%)", "Sidelap_(%)", "Speed_(Km/h)", 
            "Film_Format_Size(mm)", "Scale_(1:  )","Coordinate1_Latitude","Coordinate1_Longtitude", "Coordinate2_Latitude", "Coordinate2_Longitude",
            "Coordinate3_Latitude","Coordinate3_Longitude", "Coordinate4_Latitude", "Coordinate4_Longtitude", "",
             "Flying_Height_Above_Sea_Level(m)" "", "Minimum_Flight_Lines", "Distance_Between_Lines(m)", "", "Total_Photos", "Photos_Per_Line", "", 
             "Line_Starting_Coordinates(From start to end)"])
    else:
        print("Please confirm that you have checked your input data.")



def Digital_input_loop():  
    print()
    # Ensure user has prepared csv correctly prior to import, primarly concerning units of measure
    # This is done as an outside "data validation" to double check that the user understands what is required to run the program
    # Having the user verify the data before import prevents the need to start program over and delete csv created before validation      
    print("Focal Length = mm (e.g. 152.4)")
    print("Average Terrain Elevation Above Datum = metres above sea level (e.g. 300)")        
    print("Endlap = percantage as decimal (e.g. 0.60)")
    print("Sidelap = percentage as decimal (e.g. 0.30)")
    print("Average Ground Speed of Plane = km/hr (e.g. 160)")
    print("Across-Track Array Pixels = Total Pixels (e.g. 20010)")
    print("Along-track Array Pixels = Total Pixels (e.g. 13080")
    print("Physical Pixel Size = mm (e.g. 0.0052)")
    print("Ground Sampling Distance = m (e.g. 0.25)") 
    print("The latitude and longitude of the 4 coordinates of the corner of the study area, starting with coordinate 1 latitude")
    print("You may also use the provided input csv template.")
    print()  
    userready = input("Are you ready to import your csv and begin flight planning? (Y/N): ")
    print()
    # If user enters Y/y the program will proceed to read the input from their csv, otherwise it will end
    # Program ends instead of loops because the process of checking the data could be lengthy
    if userready.upper() == "Y":
        # prompt input for string of file path of desired csv file
        input_path = str(input("Please enter the path to your input data csv file:  "))
        # open and read csv file and append values to global lists 
        with open(input_path, "r") as input_data:
            input_read = csv.reader(input_data)
            next(input_read)
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
                coords_list[0].append(float(record[9]))
                coords_list[0].append(float(record[10]))
                coords_list[1].append(float(record[11]))
                coords_list[1].append(float(record[12]))
                coords_list[2].append(float(record[13]))
                coords_list[2].append(float(record[14]))
                coords_list[3].append(float(record[15]))
                coords_list[3].append(float(record[16]))
        # prompt input of output csv location path
        output_location = str(input("What is the file path to the folder you want the output csv to be in?:   "))
        # Call global csv variable and assign name depending on camera type
        global output_path 
        # Name output csv file according to camera type selected
        output_path = output_location + "FlightPlan-DigitalOutput.csv"
        # Open output csv file and append a header row with header
        with open(output_path, "a") as output_data:
            headwriter = csv.writer(output_data)
            headwriter.writerow(["Focal_Length(mm)", "Elevation_(meters_ASL)", "Endlap_(%)", "Sidelap_(%)", "Speed_(Km/h)", "Across_Track_Array", 
            "Along_Track_Array", "Pixel_Size(mm)", "Ground_Sampling_Distance(m)", "Coordinate1_Latitude","Coordinate1_Longtitude","Coordinate2_Latitude",
             "Coordinate2_Longitude","Coordinate3_Latitude","Coordinate3_Longitude", "Coordinate4_Latitude", "Coordinate4_Longtitude","", 
             "Flying_Height(meters_above_terrain", "Flying_Height_Above_Sea_Level(m)", "", "Minimum_Flight_Lines", "Distance_Between_Lines(m)",
              "", "Total_Photos", "Photos_Per_Line",  "", "Line_Starting_Coordinates(From start to end)"])
    else:
        print("Please confirm that you have checked your input data.")



def Film_calcandoutput_loop():
    # Data validation for film inputs
    # This segement of code establishes the acceptable ranges for each input variable and checks that the variable values are valid
    # (variable)Low and (variable)High are estbalished and the list items are checked against them
    # If the items are out of range, the (variable)Check is stored as False, having failed the validation check
    # This section is able to check csv files with multiple records

    # Check Focal Length
    focalLow, focalHigh = 3, 900
    focalCheck = True
    for item in focallength_list:
        if item < focalLow or item > focalHigh:
            focalCheck = False
            break
    # Check Elevation
    elevationLow, elevationHigh = -414, 8848
    elevationCheck = True
    for item in elevation_list:
        if item < elevationLow or item > elevationHigh:
            elevationCheck = False
            break
    # Check Endlap
    endlapLow, endlapHigh = 0, 1
    endlapCheck = True
    for item in endlap_list:
        if item <= endlapLow or item >= endlapHigh:
            endlapCheck = False
            break
    # Check Sidelap
    sidelapLow, sidelapHigh = 0, 1
    sidelapCheck = True
    for item in sidelap_list:
        if item <= sidelapLow or item >= sidelapHigh:
            sidelapCheck = False
            break
    # Check Speed
    speedLow, speedHigh = 50, 350 
    speedCheck = True
    for item in speed_list:
        if item < speedLow or item > speedHigh:
            speedCheck = False
            break
    # Check Film Format
    filmLow, filmHigh = 8, 500
    filmCheck = True
    for item in filmformatsizeinput_list:
        if item < filmLow or item > filmHigh:
            filmCheck = False
            break
    # Check Scale
    scaleLow, scaleHigh = 100, 1000000
    scaleCheck = True
    for item in scaleinput_list:
        if item < scaleLow or item > scaleHigh:
            scaleCheck = False
            break         
    # Check latitudes
    latLow, latHigh = -90, 90
    latCheck = True
    if coords_list[0][0] < latLow or coords_list[0][0] > latHigh or coords_list[1][0] < latLow or coords_list[1][0] > latHigh \
        or coords_list[2][0] < latLow or coords_list[2][0] > latHigh or coords_list[3][0] < latLow or coords_list[3][0] > latHigh:
        latCheck = False
    # Check latitudes
    longLow, longHigh = -180, 180
    longCheck = True
    if coords_list[0][1] < longLow or coords_list[0][1] > longHigh or coords_list[1][1] < longLow or coords_list[1][1] > longHigh \
        or coords_list[2][1] < longLow or coords_list[2][1] > longHigh or coords_list[3][1] < longLow or coords_list[3][1] > longHigh:
        longCheck = False   

    # Identify False checks and print message to user 
    # If any of the checks were assigned False, the following messages are printed to the user
    # The program ends if any checks are failed, otherwise the code proceeds to calculations
    if focalCheck == False :
        print("Focal Length must be greater than 7mm and less than 901mm.")
        print("Please check your data inputs.")
    elif elevationCheck == False :
        print("Elevation must be greater than -415m (Dead Sea) and less than 8849m (Mount Everest).")
        print("Please check your data inputs.")
    elif endlapCheck == False :
        print("Endlap must be greater than 0.00 and less than 1.00.")
        print("Please check your data inputs.")
    elif sidelapCheck == False :
        print("Sidelap must be greater than 0.00 and less than 1.00.")
        print("Please check your data inputs.")
    elif speedCheck == False :
        print("Speed must be greater than 49km/hr and less than 351km/hr.")
        print("Please check your data inputs.")
    elif filmCheck == False :
        print("Film Format must be greater than 7mm and less than 501mm.")
        print("Please check your data inputs.")
    elif scaleCheck == False :
        print("Scale must be greater than 99 and less than 1000001.")
        print("Please check your data inputs.")
    elif latCheck == False:
        print("Latitudes must be greater than -91 degrees and less than 91 degrees.")
        print("Please check your data inputs.")
    elif longCheck == False:
        print("Longitudes must be greater than -181 degrees and less than 181 degrees.")
        print("Please check your data inputs.")
    # Proceed with calculations having validated the input data
    else:
        # If program passes data validation, it is passed into the calculations loop
        for index in range(len(focallength_list)):
            # values from input lists are assigned to local variables for calculations
            scaleinput = scaleinput_list[index]
            filmformatsizeinput = filmformatsizeinput_list[index]
            elevation = elevation_list[index]
            focallength = focallength_list[index]
            endlap = endlap_list[index]
            sidelap = sidelap_list[index]
            speed = speed_list[index]
            coordinate1 = coords_list[0][0], coords_list[0][1]
            coordinate2 = coords_list[1][0], coords_list[1][1]
            coordinate3 = coords_list[2][0], coords_list[2][1]
            coordinate4 = coords_list[3][0], coords_list[3][1]

            # convert degrees to radians, store in list
            rcoords = [[] for x in range(4)]
            for x in range(len(coords_list)):
                for y in range(len(coords_list[x])):
                    rcoords[x].append(math.radians(coords_list[x][y]))

            # pass radian values to haversine function
            distance = haversine(rcoords)
            length = distance[0]
            width = distance[1]

            # Calcualte digital camera specific variables using equations found:
            # Lillesand, T.M., Kiefer, R.W., Chipman, J.W. (2018). Remote Sensing And Image Interpretation – Seventh Edition. Wiley.
            scale = 1/scaleinput
            filmformatsize = filmformatsizeinput/1000
            flyingheight = (focallength/1000/scale)+elevation
            singleimagegc = filmformatsize/scale
            groundphotosep = (1-endlap)*singleimagegc
            exposuretime = math.floor((groundphotosep/speed)*(3600/1000))
            adjustedgroundphotosep = exposuretime*speed*(1000/3600)
            photosperline = math.ceil((length/adjustedgroundphotosep)+1+1)
            distancebwlines = (1-sidelap)*singleimagegc
            flightlines = math.ceil((width/distancebwlines)+1)
            totalphotos = flightlines*photosperline

            linestartcoords = startingCoords(rcoords, distancebwlines, flightlines)


            #display final outputs for film camera
            print("Flying Height: ")
            print("With a camera focal length of ", focallength, " millimetres and a desired scale of 1:", scaleinput, 
            " at an average terrain elevation of ", elevation, " metres above sea level, flying height above terrain is ", flyingheight, ". \n")
            print("Minimum Flight Lines: ")
            print("With a film format size of ", filmformatsizeinput, " millimetres and scale of 1:", scaleinput, 
            ", the ground cover of a single image is ", singleimagegc, "metres on a side")
            print("With a desired sidelap of ", (sidelap*100), "%, there should be ", distancebwlines, " metres between flight lines.")
            print("With the study area wdith of ", width, " metres, the minimum number of flight lines is ", flightlines, ". \n")
            print("Minimum Numbers of Photographs: ")
            print("With a desired endlap of ", (endlap*100), "%, ground photo seperation is ", groundphotosep, " metres.")
            print("With an aircraft speed of ", speed, "km/h, time between exposures is ", exposuretime, " seconds.")
            print("With an adjusted distance of ", adjustedgroundphotosep, " metres between photographs, the minimum number of photos per line is ", 
            photosperline, ". \n")
            print("The total number of photographs taken will be ", totalphotos, ".")

            # Open output csv file and append the calculated values to a new row
            with open(output_path, "a") as output_data:
                writer = csv.writer(output_data)
                writer.writerow([focallength, elevation, endlap, sidelap, speed, filmformatsizeinput, scaleinput, coordinate1[0], coordinate1[1], coordinate2[0], 
                coordinate2[1],coordinate3[0], coordinate3[1], coordinate4[0], coordinate4[1], "", flyingheight, flightlines, 
                distancebwlines, "", totalphotos, photosperline, ""]+ linestartcoords)    


def Digital_calcandouput_loop():
    # Data validation for film inputs
    # This segement of code establishes the acceptable ranges for each input variable and checks that the variable values are valid
    # (variable)Low and (variable)High are estbalished and the list items are checked against them
    # If the items are out of range, the (variable)Check is stored as False, having failed the validation check
    # This section is able to check csv files with multiple records

    # Check Focal Length
    focalLow, focalHigh = 3, 900
    focalCheck = True
    for item in focallength_list:
        if item < focalLow or item > focalHigh:
            focalCheck = False
            break
    # Check Elevation
    elevationLow, elevationHigh = -414, 8848
    elevationCheck = True
    for item in elevation_list:
        if item < elevationLow or item > elevationHigh:
            elevationCheck = False
            break
    # Check Endlap
    endlapLow, endlapHigh = 0, 1
    endlapCheck = True
    for item in endlap_list:
        if item <= endlapLow or item >= endlapHigh:
            endlapCheck = False
            break
    # Check Sidelap
    sidelapLow, sidelapHigh = 0, 1
    sidelapCheck = True
    for item in sidelap_list:
        if item <= sidelapLow or item >= sidelapHigh:
            sidelapCheck = False
            break
    # Check Speed
    speedLow, speedHigh = 50, 350 
    speedCheck = True
    for item in speed_list:
        if item < speedLow or item > speedHigh:
            speedCheck = False
            break
    # Check Across Track Array
    acrossLow, acrossHigh = 256, 27000
    acrossCheck = True
    for item in acrosstrack_list:
        if item < acrossLow or item > acrossHigh:
            acrossCheck = False
            break
    # Check Along Track Array
    alongLow, alongHigh = 256, 27000
    alongCheck = True
    for item in alongtrack_list:
        if item < alongLow or item > alongHigh:
            alongCheck = False
            break
    # Check Pixel Size
    pixelLow, pixelHigh = 0.0008, 0.25
    pixelCheck = True
    for item in pixelsize_list:
        if item < pixelLow or item > pixelHigh:
            pixelCheck = False
            break
    # Check Ground Sampling Distance
    gsdLow, gsdHigh = 0, 25.99
    gsdCheck = True
    for item in gsd_list:
        if item < gsdLow or item > gsdHigh:
            gsdCheck = False
            break  
    # Check latitudes
    latLow, latHigh = -90, 90
    latCheck = True
    if coords_list[0][0] < latLow or coords_list[0][0] > latHigh or coords_list[1][0] < latLow or coords_list[1][0] > latHigh \
    or coords_list[2][0] < latLow or coords_list[2][0] > latHigh or coords_list[3][0] < latLow or coords_list[3][0] > latHigh:
        latCheck = False
    # Check latitudes
    longLow, longHigh = -180, 180
    longCheck = True
    if coords_list[0][1] < longLow or coords_list[0][1] > longHigh or coords_list[1][1] < longLow or coords_list[1][1] > longHigh \
    or coords_list[2][1] < longLow or coords_list[2][1] > longHigh or coords_list[3][1] < longLow or coords_list[3][1] > longHigh:
        longCheck = False              
    # Identify False checks and print message to user 
    # If any of the checks were assigned False, the following messages are printed to the user
    # The program ends if any checks are failed, otherwise the code proceeds to calculations
    if focalCheck == False :
        print("Focal Length must be greater than 2mm and less than 901mm.")
        print("Please check your data inputs.")
    elif elevationCheck == False :
        print("Elevation must be greater than -415m (Dead Sea) and less than 8849m (Mount Everest).")
        print("Please check your data inputs.")
    elif endlapCheck == False :
        print("Endlap must be greater than 0.00 and less than 1.00.")
        print("Please check your data inputs.")
    elif sidelapCheck == False :
        print("Sidelap must be greater than 0.00 and less than 1.00.")
        print("Please check your data inputs.")
    elif speedCheck == False :
        print("Speed must be greater than 49km/hr and less than 351km/hr.")
        print("Please check your data inputs.")
    elif acrossCheck == False :
        print("Across Track Array must be greater than 255 pixels and less than 270001 pixels.")
        print("Please check your data inputs.")
    elif alongCheck == False :
        print("Along Track Array must be greater than 255 pixels and less than 270001 pixels.")
        print("Please check your data inputs.")
    elif pixelCheck == False :
        print("Physical Pixel Size must be greater than 7mm and less than 501mm.")
        print("Please check your data inputs.")
    elif gsdCheck == False :
        print("Ground Sampling Distance must be greater than 0m and less than 26m.")
        print("Please check your data inputs.")
    elif latCheck == False:
        print("Latitudes must be greater than -91 degrees and less than 91 degrees.")
        print("Please check your data inputs.")
    elif longCheck == False:
        print("Longitudes must be greater than -181 degrees and less than 181 degrees.")
        print("Please check your data inputs.")
    # Proceed with calculations having validated the input data
    else:
        # If program passes data validation, it is passed into the calculations loop
        for index in range(len(focallength_list)):
            # values from input lists are assigned to local variables for calculations
            focallength = focallength_list[index]
            elevation = elevation_list[index]
            endlap = endlap_list[index]
            sidelap = sidelap_list[index]
            speed = speed_list[index]
            acrosstrack = acrosstrack_list[index]
            alongtrack = alongtrack_list[index]
            pixelsize = pixelsize_list[index]
            gsd = gsd_list[index]
            coordinate1 = coords_list[0][0], coords_list[0][1]
            coordinate2 = coords_list[1][0], coords_list[1][1]
            coordinate3 = coords_list[2][0], coords_list[2][1]
            coordinate4 = coords_list[3][0], coords_list[3][1]


            # convert degrees to radians, store in list
            rcoords = [[] for x in range(4)]
            for x in range(len(coords_list)):
                for y in range(len(coords_list[x])):
                    rcoords[x].append(math.radians(coords_list[x][y]))

            # pass radian values to haversine function
            distance = haversine(rcoords)
            length = distance[0]
            width = distance[1]

            # Calcualte digital camera specific variables using equations found:
            # Lillesand, T.M., Kiefer, R.W., Chipman, J.W. (2018). Remote Sensing And Image Interpretation – Seventh Edition. Wiley.
            flyingheight = ((gsd*focallength)/pixelsize)+elevation
            heightaboveterrain = flyingheight-elevation 
            acrosscoverage = (((acrosstrack*pixelsize)*heightaboveterrain)/focallength)
            alongcoverage = (((alongtrack*pixelsize)*heightaboveterrain)/focallength)
            groundphotosep = (1-endlap)*alongcoverage
            exposuretime = math.floor((groundphotosep/speed)*(3600/1000))
            photosperline = math.ceil((length/groundphotosep)+1+1)
            distancebwlines = (1-sidelap)*acrosscoverage
            flightlines = math.ceil((width/distancebwlines)+1)
            totalphotos = flightlines*photosperline

            linestartcoords = startingCoords(rcoords, distancebwlines, flightlines)

            #Display final outputs for digital camera
            print("Flying Height: ")
            print("With a focal length of ", focallength, " millimetres, a pixel size of ", pixelsize, 
            " millimetres, a ground sampling distance of ", gsd, " metres, and at an average terrain elevation of ", elevation, 
            " metres above sea level, flying height above terrain is ", heightaboveterrain, " metres. \n")
            print("Minimum Flight Lines: ")
            print("Across track ground coverage distance with ", acrosstrack, " pixels is ", acrosscoverage, " metres.")
            print("With a desired sidelap of ", sidelap, "%, there should be ", distancebwlines, " metres between flight lines.")
            print("With a study area width of ", width, " metres, the minimum number of flight lines is ", flightlines, ". \n")
            print("Minimum Number of Photographs: ")
            print("Along track ground coverage distance with ", alongtrack, " pixels is ", alongcoverage, " metres.")
            print("With a desired endlap of ", endlap, " %, ground photo seperation is ", groundphotosep, " metres.")
            print("With an aircraft speed of ", speed, "km/h, time between exposures is ", exposuretime, " seconds.")
            print("With a distance of ", groundphotosep, " metres between photographs, the minimum number of photos per line is ", photosperline, ". \n")
            print("The total number of photographs taken will be ", totalphotos, ".")
            # Open output csv and append the calculated values to a new row
            with open(output_path, "a") as output_data:
                writer = csv.writer(output_data)
                writer.writerow([focallength, elevation, endlap, sidelap, speed, acrosstrack, alongtrack, pixelsize, gsd, coordinate1[0], coordinate1[1], 
                coordinate2[0], coordinate2[1], coordinate3[0], coordinate3[1], coordinate4[0], coordinate4[1],"", heightaboveterrain, flyingheight, 
                "", flightlines, distancebwlines, "", totalphotos, photosperline, ""]+ linestartcoords)

    


def main():
    # Exception handling takes place once the main function is called
    # It is known that null values in the csv file will cause a ValueError
    try:
        # Display Program Purpose to the user
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
        elif cameratype.upper() == "D":
            Digital_input_loop()
            Digital_calcandouput_loop()
    # The following exceptions were added to try condition to catch any errors that might occur
    # The errors are displayed as a message, with an addition for ValueError
    except TypeError as message:
        print(" There was an error: ", message)
    except NameError as message:
        print(" There was an error: ", message)
    except ValueError as message:
        print(" There was an error: ", message)
        print(" A ValueError may result from the occurence of null values in the csv.")
    except SyntaxError as message: 
        print(" There was an error: ", message)
    except RuntimeError as message:
        print(" There was an error: ", message)
    except Exception as message:
        print(" There was an error: ", message)

if __name__ == "__main__":
    main()