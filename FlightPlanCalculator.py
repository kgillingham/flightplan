# This program will aid the designing process of an aerial photography remote sensing mission. 
# Specifically, this program will calculate the location, direction, and number of flight lines
# necessary to adequately photograph a given area, as well as the elevation the aircraft should fly at. 
import math
def main():
    print('test')

# TO DO
def haversine():
    print('test')

# TO DO
def latLongDistance():
    print('test')


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
    gsd = float(input("In metres, what is the ground smapling distance? (e.g. 0.25): ")
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



