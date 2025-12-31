from datetime import time

#Compute days since Jan 1st 4713 BCE using the Meeus method
#Note this is valid for positive and negative years, but wont work for negative Julian days
#This limits the Calculator to 4713 BCE
#Julian Days start at noon greenwhich time
def ComputeJulianDate(year, month, day):
    #Month Adjustment
    if month <= 2:              #Start counting from march and treat jan and feb as months 13 and 14. This avoids issues with leap days messing up the year
        year -= 1               #Move to previous year
        month += 12             #Make month 13 or 14

    #Adjustment for switch to gregorian calander from julian calander in 1582
    if year > 1582:
        A = int(year / 100)
        B = 2 - A + int(A / 4)
    else:
        B = 0

    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

#Takes in a sidereal degrees, and returns in a time container
#Note that using this in function can introduce computational error
def MeanSiderealDegToHour(MST_deg):
    MST_hr = MST_deg / 15.0

    #Containers
    hourCont = int(MST_hr)
    minuteCont = int((MST_hr - hourCont) * 60)
    secondsCont = int(((MST_hr - hourCont) * 60 - minuteCont) * 60)
    microsecondsCont = int(((((MST_hr - hourCont) * 60 - minuteCont) * 60 - secondsCont) * 1e6))

    MST_time = time(hour=hourCont, minute=minuteCont, second=secondsCont, microsecond=microsecondsCont)
    return MST_time


#Takes in a sidereal hour in a time container, and returns a degrees
#Note that using this in function can introduce computational error
def MeanSiderealHourToDeg(MST_Hour):
    #Break into components
    MST_hr = MST_Hour.hour + MST_Hour.minute / 60.0 + MST_Hour.second / 3600.0 + MST_Hour.microsecond / 3_600_000_000.0
    
    #Hours to degrees and normalize
    MST_deg = (MST_hr * 15.0) % 360
    
    return MST_deg

def GetSiderealFromUTC(year, month, day, longitude):
    #Calulate Julian Datetime
    JD = ComputeJulianDate(year, month, day)

    #Calulate Greenwich mean sidereal time (GMST)
    T = (JD - 2451545.0) / 36525                            #Julian centuries since epoch J2000.0 (reference epoch for positions of astrnomical objects) at 12:00
    
    GMST_deg = ((280.46061837                               #GMST since J2000.0
              + (360.98564736629 * (JD - 2451545.0))        #Degrees per julian day elapsed (sidereal days are shorter so its more than 360 degrees)
              + (0.000387933 * (T * T))                     #Precession correction
              - ((T * T * T) / 38710000.0))                 #More corrections
              % 360)                                        #Normalize to a single rotation
    
    #GMST_hr = GMST_deg / 15.0

    #Convert to local sidereal time
    LMST_deg = (GMST_deg + longitude) % 360
 
    return MeanSiderealDegToHour(LMST_deg)