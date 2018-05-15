# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:37:28 2018

@author: Taeke
"""

import matplotlib.pyplot as plt
import matplotlib #Type "%matplotlib qt"  in console to show figure in seperate window
import pickle
import os.path
import datetime
import pytz

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))
        
def get_number_of_hours_year(year): 
    if (year % 4) == 0 and (year % 100 != 0 or year % 400 == 0):
        days = 366
    else:
       days = 365
    return days * 24


mapLocation = os.getcwd() + '\\data\\RADIUS100KM'
# mapLocation = 'C:\\Users\\m_a_s\\Desktop\\data\\RADIUS100KM'

# set inputs
startYear = 2017
endYear = 2017
YEARS = range(startYear, endYear + 1)

# dfine constants
missingValue = 999.9

data_total = {}
data_total = dict.fromkeys(list(YEARS), {})

for year in YEARS:
    
    print('current year: ', year)
    
    # get path current year
    yearString = str(year)
    dataLocation = mapLocation + '\\' + yearString + '.pickle'
    datalocationStationID= mapLocation +'\\STATION_ID.pickle'
    
    
    # load data current year
    file = open(dataLocation, 'rb')
    data = pickle.load(file)
    
    # load station ID current year
    file = open(datalocationStationID, 'rb')
    stationIDs = pickle.load(file)
    
    numberOfStations = len(stationIDs)
    
    # create range of dates
    base = datetime.datetime(year, 1, 1, 0, 0, tzinfo = pytz.UTC)
    numHours = get_number_of_hours_year(year)
    dateList = [base + datetime.timedelta(hours=x) for x in range(0, numHours)]
    
    data_total[year] = dict.fromkeys(list(stationIDs), {})
    
    # loop over stations
    for ID in stationIDs[0:1]:
        
        print('current station: ', ID)
        
        # get keys from data
        currentKeys = list(data[ID].keys())
        data_total[year][ID] = dict.fromkeys(currentKeys, [])
        
        # init temperature list
        # temperatureList = [missingValue] * len(dateList)
        # temperaturesMeasurment = data[ID]['air_temperature']
        datesMeasurement = data[ID]['datetime']
        indexMeasurement = []
        
        for date in dateList:
            nearestDate = nearest(datesMeasurement, date)
            indexMeasurement.append(datesMeasurement.index(nearestDate))
            
            # store in new dictionary
        for key in currentKeys:
            data_total[year][ID][key] = data[ID][key][indexMeasurement]
            print('appending', data[ID][key][indexMeasurement], 'to key ', key)
            # temperatureList[indexPlacement] = temperaturesMeasurment[indexMeasurement]
            
            
            