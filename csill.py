###############################################################################################
####  ______             __  __  __    __                               ______  ______     ####
##   /      \           |  \|  \|  \   \_\                              |      \|      \     ##
##  |  $$$$$$\  _______  \$$| $$| $$  ______    _______  ________        \$$$$$$ \$$$$$$     ##
##  | $$   \$$ /       \|  \| $$| $$ /      \  /       \|        \        | $$    | $$       ##
##  | $$      |  $$$$$$$| $$| $$| $$|  $$$$$$\|  $$$$$$$ \$$$$$$$$        | $$    | $$       ##
##  | $$   __  \$$    \ | $$| $$| $$| $$    $$ \$$    \   /    $$         | $$    | $$       ##
##  | $$__/  \ _\$$$$$$\| $$| $$| $$| $$$$$$$$ _\$$$$$$\ /  $$$$_        _| $$_  _| $$_      ##
##   \$$    $$|       $$| $$| $$| $$ \$$     \|       $$|  $$    \      |   $$ \|   $$ \     ##
##    \$$$$$$  \$$$$$$$  \$$ \$$ \$$  \$$$$$$$ \$$$$$$$  \$$$$$$$$       \$$$$$$ \$$$$$$     ##
##                                            __                                             ##
##                                           / _|                                            ##
##                                          | |_ _ __ ___  _ __ ___                          ##
##                                          |  _| '__/ _ \| '_ ` _ \                         ##
##              _______            __       | | | | | (_) | | | | | |                        ##
##             /       \          /  |      |_| |_|  \___/|_| |_| |_|                        ##
##             $$$$$$$  | ______  $$ |  ______    ______    ______                           ##
##             $$ |__$$ |/      \ $$ | /      \  /      \  /      \                          ##
##             $$    $$/ $$$$$$  |$$ |/$$$$$$  |/$$$$$$  |/$$$$$$  |                         ##
##             $$$$$$$/  /    $$ |$$ |$$    $$ |$$    $$ |$$    $$ |                         ##
##             $$ |     /$$$$$$$ |$$ |$$$$$$$$/ $$$$$$$$/ $$$$$$$$/                          ##
##             $$ |     $$    $$ |$$ |$$       |$$       |$$       |                         ##
##             $$/       $$$$$$$/ $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/                          ##
##                                                                                           ##
##                                                                                           ##
##        > Conversion Between Coordinate Systems                                            ##
##        > Calculate Geographical Distances                                                 ##
##        > Convert Sidereal Time/Local Sidereal Time (ST, LST)                              ##
##        > Calculate Twilights' Correct Datetimes on Specific Locations                     ##
####                                                                                       ####
###############################################################################################
####                                                                                       ####
##        USED LEGENDS AND LABELS:                                                           ##
##                                                                                           ##
##        φ: Latitude                                                                        ##
##        λ: Longitude                                                                       ##
##        H: Local Hour Angle in Degrees                                                     ##
##        t: Local Hour Angle in Hours                                                       ##
##        S: Local Sidereal Time                                                             ##
##        A: Azimuth at Horizontal Coords                                                    ##
##        m: Altitude at Horizontal Coords                                                   ##
##        δ: Declination at Equatorial Coords                                                ##
##        α: Right Ascension at Equatorial Coords                                            ##
####                                                                                       ####
###############################################################################################

# If libraries are not installed, decomment and run
# pip install matplotlib --upgrade
# pip install numpy --upgrade

import math
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Current Version of the Csillész II Problem Solver
ActualVersion = 'v0.9'

######## CONSTANTS FOR CALCULATIONS ########

# Earth's Radius
R = 6378e03

# Lenght of 1 Solar Day = 1.002737909350795 Sidereal Days
# It's Usually Labeled dS/dm
# We Simply Label It dS
dS = 1.002737909350795

# Predefined Coordinates of Some Notable Cities
CityDict = {
"Beijing": [39.9042,116.4074],
"Budapest": [47.4979,19.0402],
"Budakeszi": [47.5136,18.9278],
"Budaors": [47.4621,18.9530],
"Brussels": [50.8503,4.3517],
"Debrecen": [47.5316,21.6273],
"Gyor": [47.6875,17.6504],
"Jerusalem": [31.7683,35.2137],
"Kecskemet": [46.8964,19.6897],
"Mako": [46.2219,20.4809],
"Miskolc": [48.1035,20.7784],
"Nagykanizsa": [46.4590,16.9897],
"NewYork": [40.7128,-74.0060],
"Pecs": [46.0727,18.2323],
"Rio": [-22.9068,-43.1729],
"Szeged": [46.2530,20.1414],
"Szeghalom": [47.0239,21.1667],
"Szekesfehervar": [47.1860,18.4221],
"Tokyo": [35.6895,139.6917],
"Washington": [47.7511,-120.7401],
"Zalaegerszeg": [46.8417,16.8416]
}

# Months' length int days, without leap day
MonthLengthList = [31,28,31,30,31,30,31,31,30,31,30,31]

# Months' length int days, with leap day
MonthLengthListLeapYear = [31,28,31,30,31,30,31,31,30,31,30,31]

######## UTILITY FUNCTIONS ########

# Normalization with Bound [0,NonZeroBound]
def NormalizeZeroBounded(Parameter, NonZeroBound):

    if(Parameter >= 0):
        Parameter = Parameter - (int(Parameter / NonZeroBound) * NonZeroBound)
    else:
        Parameter = Parameter + ((int(Parameter / NonZeroBound) + 1) * NonZeroBound)

    return(Parameter)

# Normalization Between to [-π/2,+π/2]
def NormalizeSymmetricallyBoundedPI(Parameter):
    
    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter < 0):
        if(Parameter < -90 and Parameter >= -270):
            Parameter = - (Parameter + 180)
        elif(Parameter < -270 and Parameter >= -360):
            Parameter = Parameter + 360

    elif(Parameter > 0):
        if(Parameter > 90 and Parameter <= 270):
            Parameter = - (Parameter - 180)
        elif(Parameter > 270 and Parameter <= 360):
            Parameter = Parameter - 360

    return(Parameter)

# Normalization Between to [-π,+π]
def NormalizeSymmetricallyBoundedPI_2(Parameter):

    if(Parameter <= -360 or Parameter >= 360):
        Parameter = NormalizeZeroBounded(Parameter, 360)

    if(Parameter <= -180 or Parameter >= 180):
        Parameter = 180 - Parameter

    return(Parameter)


######## 1. CONVERSION OF COORDINATE SYSTEMS ########

# 1. Horizontal to Equatorial I
def HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime=None):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Altitude: [-π/2,+π/2]
    # Azimuth: [0,2π]
    # Local Sidereal Time: [0,24h]
    Latitude = NormalizeSymmetricallyBoundedPI_2(Latitude)
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)
    Azimuth = NormalizeZeroBounded(Azimuth, 360)
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)
    
    # Calculate Declination (δ)
    # sin(δ) = sin(m) * sin(φ) + cos(m) * cos(φ) * cos(A)
    Declination =  math.degrees(math.asin(
                   math.sin(math.radians(Altitude)) * math.sin(math.radians(Latitude)) +
                   math.cos(math.radians(Altitude)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(Azimuth))))
    # Normalize result for Declination [-π/2,+π/2]
    Declination = NormalizeSymmetricallyBoundedPI(Declination)

    # Calculate Local Hour Angle in Degrees (H)
    # sin(H) = - sin(A) * cos(m) / cos(δ)
    LocalHourAngleDegrees = math.degrees(math.asin(
                            - math.sin(math.radians(Azimuth)) * math.cos(math.radians(Altitude)) / math.cos(math.radians(Declination))))
    # Normalize result [0,+2π]
    LocalHourAngleDegrees = NormalizeZeroBounded(LocalHourAngleDegrees, 360)
    # Convert to hours from angles (H -> t)
    LocalHourAngle = LocalHourAngleDegrees / 15

    if(LocalSiderealTime != None):
        # Calculate Right Ascension (α)
        # α = S – t
        RightAscension = LocalSiderealTime - LocalHourAngle
    else:
        RightAscension = None

    return(Declination, LocalHourAngle, RightAscension)

# 2. Horizontal to Equatorial II
def HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime):

    # First Convert Horizontal to Equatorial I Coordinates
    Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

    # Convert Equatorial I to Equatorial II
    LocalSiderealTime = LocalHourAngle + RightAscension

    return(Declination, LocalSiderealTime)


# 3. Equatorial I to Horizontal
def EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime, LocalHourAngle):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Right Ascension: [0h,24h[
    # Declination: [-π/2,+π/2]
    Latitude = NormalizeSymmetricallyBoundedPI_2(Latitude)
    RightAscension = NormalizeZeroBounded(RightAscension, 24)
    Declination = NormalizeSymmetricallyBoundedPI(Declination)  

    if(LocalHourAngle == None):
        # Calculate Local Hour Angle in Hours (t)
        # t = S - α
        LocalHourAngle = LocalSiderealTime - RightAscension
    # Convert to angles from hours (t -> H)
    LocalHourAngleDegrees = LocalHourAngle * 15

    # Calculate Altitude (m)
    # sin(m) = sin(δ) * sin(φ) + cos(δ) * cos(φ) * cos(H)
    Altitude = math.degrees(math.asin(
               math.sin(math.radians(Declination)) * math.cos(math.radians(Latitude)) + 
               math.cos(math.radians(Declination)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(LocalHourAngleDegrees))))

    # Calculate Azimuth (A)
    # sin(A) = - sin(H) * cos(δ) / cos(m)
    Azimuth = math.degrees(math.asin(
              - math.sin(math.radians(LocalHourAngleDegrees)) * math.cos(math.radians(Declination)) / math.cos(math.radians(Altitude))))

    return(Altitude, Azimuth)

# 4. Equatorial I to Equatorial II
def EquIToEquII(RightAscension, LocalHourAngle):
    
    LocalSiderealTime = LocalHourAngle + RightAscension

    return(LocalSiderealTime)

# 5. Equatorial II to Equatorial I
def EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle):

    # Calculate Right Ascension or Local Sidereal Time
    if(RightAscension != None and LocalSiderealTime == None):
        LocalHourAngle = LocalSiderealTime - RightAscension

    elif(RightAscension == None and LocalSiderealTime != None):
        RightAscension = LocalSiderealTime - LocalHourAngle
    
    else:
        pass

    return(LocalHourAngle, RightAscension)

# 6. Equatorial II to Horizontal
def EquIIToHor(Latitude, LocalSiderealTime, LocalHourAngle, RightAscension, Declination):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Local Sidereal Time: [0h,24h[
    # Local Hour Angle: [0h,24h[
    # Right Ascension: [0h,24h[
    # Declination: [-π/2,+π/2]
    Latitude = NormalizeSymmetricallyBoundedPI(Latitude)
    LocalSiderealTime = NormalizeZeroBounded(LocalSiderealTime, 24)
    
    if(RightAscension == None and LocalSiderealTime != None):
        LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)

    elif(RightAscension != None and LocalSiderealTime == None):
        RightAscension = NormalizeZeroBounded(RightAscension, 24)
    
    Declination = NormalizeSymmetricallyBoundedPI_2(Declination)

    # Convert Equatorial II to Equatorial I
    LocalHourAngle, RightAscension = EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle)

    # Normalization of Output Data
    LocalHourAngle = NormalizeZeroBounded(LocalHourAngle, 24)
    RightAscension = NormalizeZeroBounded(RightAscension, 24)

    # Convert Equatorial I to Horizontal
    Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, LocalHourAngle, LocalSiderealTime)

    # Normalization of Output Data
    # Altitude: [-π/2,+π/2]
    # Azimuth: [0,2π]
    Altitude = NormalizeSymmetricallyBoundedPI_2(Altitude)
    Azimuth = NormalizeZeroBounded(Azimuth, 360)

    return(Altitude, Azimuth)


######## 2. GEOGRAPHICAL DISTANCE ########

# Calculate distances between coordinates
def GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2):
    
    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π]
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 − hav_1))
    # Step 3.: d = R * hav_2

    # Step 1
    hav_1 = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    hav_2 = 2 * math.atan2(math.sqrt(hav_1), math.sqrt(1-hav_1))

    # Step 3
    Distance = R * hav_2

    return(Distance)


# Calculate distances between choosen cities
def GeogDistCityCalc(Latitude1, Latitude2, Longitude1, Longitude2):

    # Initial Data Normalization
    # Latitude: [-π,+π]
    # Longitude: [0,+2π]
    Latitude1 = NormalizeSymmetricallyBoundedPI(Latitude1)
    Latitude2 = NormalizeSymmetricallyBoundedPI(Latitude2)
    Longitude1 = NormalizeZeroBounded(Longitude1, 360)
    Longitude2 = NormalizeZeroBounded(Longitude2, 360)

    # Haversine formula:
    # Step 1.: hav_1 = (sin((φ2 - φ1) / 2))^2 + cos(φ1) ⋅ cos(φ2) ⋅ (sin((λ2 - λ1) / 2))^2
    # Step 2.: hav_2 = 2 * atan2(sqrt(hav_1),sqrt(1 − hav_1))
    # Step 3.: d = R * hav_2

    # Step 1
    hav_1 = ((math.sin(math.radians(Latitude2 - Latitude1) / 2))**2 +
        (math.cos(math.radians(Latitude1)) * math.cos(math.radians(Latitude2)) * (math.sin(math.radians(Longitude2 - Longitude1) / 2))**2))

    # Step 2
    hav_2 = 2 * math.atan2(math.sqrt(hav_1), math.sqrt(1-hav_1))

    # Step 3
    Distance = R * hav_2

    return(Distance)


######## 3. CALCULATE LOCAL SIDEREAL TIME (LST) ########

# Calculate Greenwich Mean Sidereal Time (GMST = S_0) at UT 00:00 on Given Date
def CalculateGMST(Longitude, UnitedHours, UnitedMinutes, UnitedDateYear, UnitedDateMonth, UnitedDateDay):

    # Days = UT days since J2000.0, including parts of a day
    # Could be + or - or 0
    Dwhole = 367 * UnitedDateYear - int(7 * (UnitedDateYear + int((UnitedDateMonth + 9) / 12)) / 4) + int(275 * UnitedDateMonth / 9) + UnitedDateDay - 730531.5
    # Dfrac = (UnitedHours + UnitedMinutes/60)/24
    Dfrac = 0 # Now UT = 00:00
    Days = Dwhole + Dfrac

    # Number of Julian centuries since J2000.0
    JulianCenturies = Days / 36525

    # Calculate GMST in Degrees
    GMSTDegrees = 280.46061837 + 360.98564736629 * Days + 0.000388 * JulianCenturies**2

    # Normalize between to [0,+2π]
    GMSTDegrees = NormalizeZeroBounded(GMSTDegrees, 360)

    # Convert GMST to Hours
    GMST = GMSTDegrees / 15

    return(GMST)

# Calculate 
def SiderealFromInput(Longitude, LocalHours, LocalMinutes, DateYear, DateMonth, DateDay):

    # Initial Data Normalization
    # Longitude: [0,+2π]
    Longitude = NormalizeZeroBounded(Longitude, 360)

    # Calculate United Time
    LocalTime = LocalHours + LocalMinutes/60

    # Summer/Winter Saving time
    # Summer: March 26/31 - October 8/14 LT+1
    # Winter: October 8/14 - March 26/31 LT+0
    if((DateMonth > 3 and DateMonth < 10) or ((DateMonth == 3 and DateDay >=25) or (DateMonth == 10 and (DateDay >= 8 and DateDay <=14)))):
        UnitedTime = LocalTime - (int(Longitude/15) + 1)
    else:
        UnitedTime = LocalTime - int(Longitude/15)

    if(UnitedTime < 0):
        UnitedHours = 24 - int(UnitedTime)
        UnitedDateDay = DateDay - 1
        if(UnitedDateDay <= 0):
            UnitedDateMonth = DateMonth - 1
            if(UnitedDateMonth == 0):
                UnitedDateMonth = 12
                UnitedDateYear = DateYear - 1
            if(DateYear%4 == 0 and DateYear%400 != 0):
                UnitedDateDay = MonthLengthListLeapYear[UnitedDateMonth - 1]
            else:
                UnitedDateDay = MonthLengthList[UnitedDateMonth - 1]

    elif(UnitedTime >= 24):
        UnitedHours = int(UnitedTime) - 24
        UnitedDateDay = DateDay + 1
        if(DateYear%4 == 0 and DateYear%400 != 0):
            if(UnitedDateDay >= MonthLengthListLeapYear[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
        else:
            if(UnitedDateDay >= MonthLengthList[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
        if(UnitedDateMonth == 13):
            UnitedDateMonth = 1
            UnitedDateYear = DateYear + 1
    else:
        UnitedHours = int(UnitedTime)
        UnitedMinutes = int((UnitedTime - UnitedHours) * 60)
        UnitedDateYear = DateYear
        UnitedDateMonth = DateMonth
        UnitedDateDay = DateDay
    
    # Calculate Greenwich Mean Sidereal Time (GMST)
    S_0 = CalculateGMST(Longitude, UnitedHours, UnitedMinutes, UnitedDateYear, UnitedDateMonth, UnitedDateDay)

    # Greenwich Zero Time for Supervision
    GreenwichHours = int(S_0)
    GreenwichMinutes = int((S_0 - GreenwichHours) * 60)
    GreenwichSeconds = int(((S_0 - GreenwichHours) - GreenwichMinutes) * 60)

    # Calculate LST
    LST = S_0 + Longitude/15 + dS * UnitedTime

    # Norm LST
    LSTNorm = NormalizeZeroBounded(LST, 24)

    LocalSiderealHours = int(LSTNorm)
    LocalSiderealMinutes = int((LocalSiderealHours - LocalSiderealHours) * 60)

    return(LocalSiderealHours, LocalSiderealMinutes, UnitedHours, UnitedMinutes, GreenwichHours, GreenwichMinutes, GreenwichSeconds)

def SiderealFromPredefined(Longitude, LocalHours, LocalMinutes, DateYear, DateMonth, DateDay):

    # Initial Data Normalization
    # Longitude: [0,+2π]
    Longitude = NormalizeZeroBounded(Longitude, 360)

    # Calculate United Time
    LocalTime = LocalHours + LocalMinutes/60
    UnitedTime = LocalTime - int(Longitude/15)

    # 
    if(UnitedTime < 0):
        UnitedHours = 24 - int(UnitedTime)
        UnitedDateDay = DateDay - 1
        if(UnitedDateDay <= 0):
            UnitedDateMonth = DateMonth - 1
            if(UnitedDateMonth == 0):
                UnitedDateMonth = 12
                UnitedDateYear = DateYear - 1
            if(DateYear%4 == 0 and DateYear%400 != 0):
                UnitedDateDay = MonthLengthListLeapYear[UnitedDateMonth - 1]
            else:
                UnitedDateDay = MonthLengthList[UnitedDateMonth - 1]

    elif(UnitedTime >= 24):
        UnitedHours = int(UnitedTime) - 24
        UnitedDateDay = DateDay + 1
        if(DateYear%4 == 0 and DateYear%400 != 0):
            if(UnitedDateDay >= MonthLengthListLeapYear[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
        else:
            if(UnitedDateDay >= MonthLengthList[DateMonth - 1]):
                UnitedDateMonth = DateMonth + 1
        if(UnitedDateMonth == 13):
            UnitedDateMonth = 1
            UnitedDateYear = DateYear + 1
    else:
        UnitedHours = int(UnitedTime)
        UnitedMinutes = int((UnitedTime - UnitedHours) * 60)
        UnitedDateYear = DateYear
        UnitedDateMonth = DateMonth
        UnitedDateDay = DateDay

    # Calculate Greenwich Mean Sidereal Time (GMST)
    S_0 = CalculateGMST(Longitude, UnitedHours, UnitedMinutes, UnitedDateYear, UnitedDateMonth, UnitedDateDay)

    # Greenwich Zero Time for Supervision
    GreenwichHours = int(S_0)
    GreenwichMinutes = int((S_0 - GreenwichHours) * 60)
    GreenwichSeconds = int(((S_0 - GreenwichHours) * 60 - GreenwichMinutes) * 60)

    # Calculate LST
    LST = S_0 + Longitude/15 + dS * UnitedTime
    
    # Norm LST
    LSTNorm = NormalizeZeroBounded(LST, 24)
    print("LSTNorm: ", LSTNorm)

    LocalSiderealHours = int(LSTNorm)
    LocalSiderealMinutes = int((LSTNorm - LocalSiderealHours) * 60)

    return(LocalSiderealHours, LocalSiderealMinutes, UnitedHours, UnitedMinutes, GreenwichHours, GreenwichMinutes, GreenwichSeconds)


###############################################################################################
####               ...     ..      ..                    .                                 ####
##               x*8888x.:*8888: -"888:                 @88>                                 ##
##              X   48888X `8888H  8888                 %8P      u.    u.                    ##
##             X8x.  8888X  8888X  !888>        u        .     x@88k u@88c.                  ##
##             X8888 X8888  88888   "*8%-    us888u.   .@88u  ^"8888""8888"                  ##
##             '*888!X8888> X8888  xH8>   .@88 "8888" ''888E`   8888  888R                   ##
##               `?8 `8888  X888X X888>   9888  9888    888E    8888  888R                   ##
##               -^  '888"  X888  8888>   9888  9888    888E    8888  888R                   ##
##                dx '88~x. !88~  8888>   9888  9888    888E    8888  888R                   ##
##              .8888Xf.888x:!    X888X.: 9888  9888    888&   "*88*" 8888"                  ##
##             :""888":~"888"     `888*"  "888*""888"   R888"    ""   'Y"                    ##
##                 "~'    "~        ""     ^Y"   ^Y'     ""                                  ##
####                                                                                       ####
###############################################################################################
###  ####                                                                             ####  ###
  ####  ###                                                                         ###  ####
        ##                                                                           ##
  #   ###                                                                             ###   #
   ####                                                                                 ####

STARTMSG = ">>> Csillész II Problem Solver Program {0}\n"
print(STARTMSG.format(ActualVersion))

while(True):

    print(">> MAIN MENU <<")
    print("(1) Coordinate System Conversion")
    print("(2) Geographical Distances")
    print("(3) Local Sidereal Time")
    print("(4) Datetimes of Twilights")
    print("(Q) Quit Program\n")

    # Choose mode by user input
    mode = input("> Choose a mode and press enter...:")
    print('\n\n')

    if(mode == '1'):
        while(True):
            print(">> Coordinate System Conversion")
            print(">> Please choose which coordinate system conversion you'd like to make!")
            print("(1) Horizontal to Equatorial I")
            print("(2) Horizontal to Equatorial II")
            print("(3) Equatorial I to Horizontal")
            print("(4) Equatorial I to Equatorial II")
            print("(5) Equatorial II to Equatorial I")
            print("(6) Equatorial II to Horizontal")
            print("(Q) Quit to Main Menu\n")
            CoordMode = input("> Choose a number and press enter...:")

            if(CoordMode == '1'):
                print(">> Conversion from Horizontal to Equatorial I Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))
                
                print("Is Local Sidereal Time given?")
                while(True):
                    HorToEquIChoose = input("Write \'Y\' or \'N\' (Yes or No)")
                    if(HorToEquIChoose == 'Y' or HorToEquIChoose == 'y' or HorToEquIChoose == 'Yes' or HorToEquIChoose == 'yes' or HorToEquIChoose == 'YEs' or HorToEquIChoose == 'yEs' or HorToEquIChoose == 'yeS' or HorToEquIChoose == 'YeS' or HorToEquIChoose == 'yES'):
                        LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                        break
                    elif(HorToEquIChoose == 'N' or HorToEquIChoose == 'n' or HorToEquIChoose == 'No' or HorToEquIChoose == 'no' or HorToEquIChoose == 'nO'):
                        LocalSiderealTime = None
                        break
                    else:
                        print("Invalid option!")

                Declination, LocalHourAngle, RightAscension = HorToEquI(Latitude, Altitude, Azimuth, LocalSiderealTime)

                # Print Results
                print("\n> Calculated parameters:")
                
                declinmsg = "- Declination (δ): {0}°"
                hourangmsg = "- Local Hour Angle (t): {0} h"
                print(declinmsg.format(Declination))
                print(hourangmsg.format(LocalHourAngle))
                
                if(LocalSiderealTime != None):
                    RAmsg = "- Right Ascension (α):  {0} h"
                    print(RAmsg.format(RightAscension))

                print('\n')

            elif(CoordMode == '2'):
                print(">> Conversion from Horizontal to Equatorial II Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                Altitude = float(input("> Altitude (m): "))
                Azimuth = float(input("> Azimuth (A): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                Declination, LocalSiderealTime = HorToEquII(Latitude, Altitude, Azimuth, LocalSiderealTime)

                # Print Results
                print("\n> Calculated Parameters:")
                
                declinmsg = "- Declination (δ): {0}°"
                sidermsg = "- Local Sidereal Time (S):  {0}°"
                print(declinmsg.format(Declination))
                print(sidermsg.format(LocalSiderealTime))
                print('\n')
                
            elif(CoordMode == '3'):
                print(">> Conversion from Equatorial I to Horizontal Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                RightAscension = float(input("> Right Ascension (α): "))
                Declination = float(input("> Declination (δ): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                LocalHourAngle = float(input("> Local Hour Angle (t): "))

                Altitude, Azimuth = EquIToHor(Latitude, RightAscension, Declination, LocalSiderealTime, LocalHourAngle)

                # Print Results
                print("\n> Calculated Parameters:")
                
                altitmsg = "- Altitude (m): {0}°"
                azimmsg = "- Azimuth (A):  {0}°"
                print(altitmsg.format(Altitude))
                print(azimmsg.format(Azimuth))
                print('\n')

            elif(CoordMode == '4'):
                print(">> Conversion from Equatorial I to Equatorial II Coordinate System")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                RightAscension = float(input("> Right Ascension (α): "))
                Declination = float(input("> Declination (δ): "))
                LocalHourAngle = float(input("> Local Hour Angle in Hours (t): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))

                LocalSiderealTime = EquIToEquII(RightAscension, LocalHourAngle)

                # Print Results
                print("\n> Calculated Parameters:")
                
                latmsg = "- Latitude (φ): {0}°"
                declinmsg = "- Declination (δ): {0}°"
                sidermsg = "- Local Sidereal Time (S):  {0}°"
                print(latmsg.format(Latitude))
                print(declinmsg.format(Declination))
                print(sidermsg.format(LocalSiderealTime))
                print('\n')

            elif(CoordMode == '5'):
                print(">> Conversion from Equatorial II to Equatorial I")
                print(">> Give Parameters: ")
                Declination = float(input("> Declination (δ): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                
                while(True):
                    print("Which Parameter Is given?")
                    EquIIChoose = input("Rigth Ascension (write \'A\'), or Local Hour Angle in Hours (write \'T\')?: ")
                    if(EquIIChoose == 'A' or EquIIChoose == 'a'):
                        LocalHourAngle = None
                        RightAscension = float(input("> Right Ascension (α): "))
                        break

                    elif(EquIIChoose == 'T' or EquIIChoose == 't'):
                        LocalHourAngle = float(input("> Local Hour Angle in Hours (t): "))
                        RightAscension = None
                        break

                    else:
                        print("Invalid option! Write \'A\' or \'T\'!")

                LocalHourAngle, RightAscension = EquIIToEquI(LocalSiderealTime, RightAscension, LocalHourAngle)

                # Print Results
                print("\n> Calculated parameters:")

                declinmsg = "- Declination (δ): {0}°"
                hourangmsg = "- Local Hour Angle (t): {0} h"

                print(declinmsg.format(Declination))
                print(hourangmsg.format(LocalHourAngle))

                if(LocalSiderealTime != None):
                    RAmsg = "- Right Ascension (α):  {0} h"
                    print(RAmsg.format(RightAscension))

                print('\n')

            elif(CoordMode == '6'):
                print(">> Conversion from Equatorial II to Horizontal")
                print(">> Give Parameters: ")
                Latitude = float(input("> Latitude (φ): "))
                LocalSiderealTime = float(input("> Local Sidereal Time (S): "))
                Declination = float(input("> Declination (δ): "))
                
                while(True):
                    print("Which Parameter Is given?")
                    EquIIChoose = input("Rigth Ascension (write \'A\'), or Local Hour Angle in Hours (write \'T\')?: ")
                    if(EquIIChoose == 'A' or EquIIChoose == 'a'):
                        LocalHourAngle = None
                        RightAscension = float(input("> Right Ascension (α): "))
                        break

                    elif(EquIIChoose == 'T' or EquIIChoose == 't'):
                        LocalHourAngle = float(input("> Local Hour Angle in Hours (t): "))
                        RightAscension = None
                        break

                    else:
                        print("Invalid option! Write \'A\' or \'T\'!")

                Altitude, Azimuth = EquIIToHor(Latitude, LocalSiderealTime, LocalHourAngle, RightAscension, Declination)

                # Print Results
                print("> Calculated Parameters:")

                altitmsg = "- Altitude (m): {0}°"
                azimmsg = "- Azimuth (A):  {0}°"
                print(altitmsg.format(Altitude))
                print(azimmsg.format(Azimuth))
                print('\n')

            elif(CoordMode == 'Q' or CoordMode == 'q'):
                break

            else:
                print("Invalid option! Try again!\n")


    elif(mode == '2'):
        while(True):
            print(">> Geographical Distance Calculator\n")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Positional Coordinates from User Input")
            print("(2) Positional Coordinates of Predefined Cities")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...:")

            print()
            if(DistMode == '1'):
                print(">> Calculate Distance from given Coordinates\n")
                print(">> Give Parameters: ")
                Latitude1 = float(input("> Latitude #1 (φ1): "))
                Longitude1 = float(input("> Longitude #1 (λ1): "))
                Latitude2 = float(input("> Latitude #2 (φ2): "))
                Longitude2 = float(input("> Longitude #2 (λ2): "))

                Distance = GeogDistCalc(Latitude1, Latitude2, Longitude1, Longitude2)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0}°,{1}°\n>>> and\n>>> {2}°,{3}°\n>>> is\n>>> {4} m\n"
                print(distmsg.format(Latitude1,Longitude1,Latitude2,Longitude2, Distance))

            elif(DistMode == '2'):
                print(">> Calculate Distance of Choosen Predefined Cities\n")
                print(">> Write the Names to the Input of Two Choosen Cities!")
                while(True):
                    City1 = input("City #1: ")

                    try:
                        Latitude1 = CityDict[City1][0]
                        Longitude1 = CityDict[City1][1]

                    except KeyError:
                        print(">>>> ERROR: The city, named \"" + City1 + "\" is not in the database")

                    break

                while(True):
                    City2 = input("City #2: ")
                    
                    try:
                        Latitude2 = CityDict[City2][0]
                        Longitude2 = CityDict[City2][1]

                    except KeyError:
                        print(">>>> ERROR: The city, named \"" + City2 + "\" is not in the database")

                    break

                Distance = GeogDistCityCalc(Latitude1, Latitude2, Longitude1, Longitude2)

                distmsg = "\n>>> The Geographical Distance Between\n>>> {0} and {1} is\n>>> {2} m\n"
                print(distmsg.format(City1, City2, Distance))

            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print("Invalid option! Try again!")


    elif(mode == '3'):
        while(True):
            print(">> Local Sidereal Time Calculator\n")
            print(">> Please choose a mode you'd like to use!")
            print("(1) Parameters from User Input")
            print("(2) Parameters of Predefined Cities")
            print("(Q) Quit to Main Menu")
            DistMode = input("> Choose a mode and press enter...:")

            print()
            if(DistMode == '1'):
                print(">> Calculate LST from given Parameters\n")
                print(">> Give Parameters: ")
                
                # Input Positional Parameters
                Latitude = float(input("> Latitude (φ): "))
                Longitude = float(input("> Longitude (λ): "))
                
                # Input Time Parameters
                while(True):
                    DateYear = int(input("> Year: "))
                    if(DateYear != 0):
                        break
                    else:
                        print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")
                
                while(True):
                    DateMonth = int(input("> Month: "))
                    if(DateMonth > 0 and DateMonth < 13):
                        break
                    else:
                        print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

                while(True):
                    DateDay = int(input("> Day: "))
                    if(DateYear%4 == 0 and DateYear%400 != 0):
                        if(MonthLengthListLeapYear[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))
                    else:
                        if(MonthLengthList[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))

                while(True):
                    LocalHours = int(input("> Local Hours: "))
                    if(LocalHours >= 0 and LocalHours <= 23):
                        break
                    else:
                        print(">>>> ERROR: Hours should be inside [0,23] interval, and should be Integer!\n")

                while(True):
                    LocalMinutes = int(input("> Local Minutes: "))
                    if(LocalMinutes >= 0 and LocalMinutes <= 59):
                        break
                    else:
                        print(">>>> ERROR: Minutes should be inside [0,59] interval, and should be Integer!\n")

                LocalSiderealHours, LocalSiderealMinutes, UnitedHours, UnitedMinutes, GreenwichHours, GreenwichMinutes, GreenwichSeconds = SiderealFromInput(Longitude, LocalHours, LocalMinutes, DateYear, DateMonth, DateDay)

                sidmsg = "\n>>> The Local Sidereal Time\n>>> at {0}h {1}m UT, at location\n>>> {2}°,{3}° with\n>>> GMST {4}h {5}m {6}s at UT 0h 0m\n>>> is {7}h {8}m\n\n"
                print(sidmsg.format(UnitedHours, UnitedMinutes, Latitude, Longitude, GreenwichHours, GreenwichMinutes, GreenwichSeconds, LocalSiderealHours, LocalSiderealMinutes))

            elif(DistMode == '2'):
                print(">> Calculate LST from the Coordinates of a Predefined City\n")
                print(">> Write the Name to the Input of a Choosen City!")

                # Input Choosen City's Name
                while(True):
                    City = input("> City's name: ")
                    try:
                        Longitude = CityDict[City][1]

                    except KeyError:
                        print(">>>> ERROR: The city, named \"" + City + "\" is not in the database")

                    break

                # Input Time Parameters
                while(True):
                    DateYear = int(input("> Year: "))
                    if(DateYear != 0):
                        break
                    else:
                        print(">>>> ERROR: Year 0 is not defined! Please write another date!\n")
                
                while(True):
                    DateMonth = int(input("> Month: "))
                    if(DateMonth > 0 and DateMonth < 13):
                        break
                    else:
                        print(">>>> ERROR: Months should be inside [1,12] interval, and should be Integer!\n")

                while(True):
                    DateDay = int(input("> Day: "))
                    if(DateYear%4 == 0 and DateYear%400 != 0):
                        if(MonthLengthListLeapYear[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))
                    else:
                        if(MonthLengthList[DateMonth - 1] >= DateDay and DateDay > 0):
                            break
                        else:
                            daysmsg = ">>>> ERROR: Days should be inside [1,{0}] interval, and should be Integer!\n"
                            print(daysmsg.format(MonthLengthListLeapYear[DateMonth - 1]))

                while(True):
                    LocalHours = int(input("> Local Hours: "))
                    if(LocalHours >= 0 and LocalHours <= 23):
                        break
                    else:
                        print(">>>> ERROR: Hours should be inside [0,23] interval, and should be Integer!\n")

                while(True):
                    LocalMinutes = int(input("> Local Minutes: "))
                    if(LocalMinutes >= 0 and LocalMinutes <= 59):
                        break
                    else:
                        print(">>>> ERROR: Minutes should be inside [0,59] interval, and should be Integer!\n")

                LocalSiderealHours, LocalSiderealMinutes, UnitedHours, UnitedMinutes, GreenwichHours, GreenwichMinutes, GreenwichSeconds = SiderealFromPredefined(Longitude, LocalHours, LocalMinutes, DateYear, DateMonth, DateDay)

                sidmsg = "\n>>> The Local Sidereal Time at {0}h {1}m UT\n>>> in {2} with\n>>> GMST {3}h {4}m {5}s at UT 0h 0m\n>>> is {6}h {7}m\n\n"
                print(sidmsg.format(UnitedHours, UnitedMinutes, City, GreenwichHours, GreenwichMinutes, GreenwichSeconds, LocalSiderealHours, LocalSiderealMinutes))

            elif(DistMode == 'Q' or DistMode == 'q'):
                break

            else:
                print("Invalid option! Try again!")

    elif(mode == '4'):
        while(True):

            print(">> Calculate Datetimes of Twilights at Specific Location")
            print(">> Give Parameters")

    elif(mode == 'Q' or mode == 'q'):
        print("All Rights Reserved to Balage Paliere Co.!")
        exit()

    else:
        print("Invalid option! Try again!")