import sys
import os
from datetime import datetime, timezone, timedelta

currentFilePath = os.path.dirname(__file__)
topLevelDir = os.path.join(currentFilePath, "..")
sys.path.append(
    os.path.abspath(topLevelDir)
)

import TimeCalc


#Test Julian Calculations
def JulianTest():
    testDates = [
        (2000, 1, 1.5, 2451545.0),
        (1999, 1, 1.0, 2451179.5),
        (1987, 1, 27.0, 2446822.5),
        (1987, 6, 19.5, 2446966.0),
        (1988, 1, 27.0, 2447187.5),
        (1988, 6, 19.5, 2447332.0),
        (1900, 1, 1.0, 2415020.5),
        (1600, 1, 1.0, 2305447.5),
        (1600, 12, 31.0, 2305812.5),
        (837, 4, 10.3, 2026871.8),
        (-123, 12, 31.0, 1676496.5),
        (-122, 1, 1.0, 1676497.5),
        (-1000, 7, 12.5, 1356001.0),
        (-1000, 2, 29.0, 1355866.5),
        (-1001, 8, 17.9, 1355671.4),
        (-4712, 1, 1.5, 0.0)
    ]
    for year, month, day, trueJD in testDates:
        calculatedJD = TimeCalc.ComputeJulianDate(year, month, day)
        error = calculatedJD - trueJD
        print(f"Date: {year}-{month}-{day}, Calculated JD: {calculatedJD}, True JD: {trueJD}, Error: {error}")

#Test Sidereal Calclation
def LST_Test():
    #Get UTC time (assumes system time is correct)
    localTime = datetime.now().astimezone()
    utcTime = localTime.astimezone(timezone.utc)

    #Get decimals of time
    currentYear = utcTime.year
    currentMonth = utcTime.month
    currentDay = utcTime.day + utcTime.hour/24 + utcTime.minute/1440 + utcTime.second/86400 + utcTime.microsecond/86400000000

    siderealTime = TimeCalc.GetSiderealFromUTC(currentYear, currentMonth, currentDay, -93.258133)
    print(siderealTime)

    for i in range(3):
        siderealDeg = TimeCalc.MeanSiderealHourToDeg(siderealTime)
        print(siderealDeg)
        siderealTime = TimeCalc.MeanSiderealDegToHour(siderealDeg)
        print(siderealTime)


#JulianTest()
LST_Test()