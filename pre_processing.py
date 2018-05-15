# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:37:28 2018

@author: Taeke
"""


#INPUTS
startYear = 2015
endYear = 2017 #downloads UPTILL endyear
RADIUS = '70' #ASSSUMES DATA IN /deepLearning/data

import numpy as np
import pickle
import os.path
import datetime
import pytz
from find_stations_unusable_temperatures import find_stations_unusable_temperatures

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))
        
def get_number_of_hours_year(year): 
    if (year % 4) == 0 and (year % 100 != 0 or year % 400 == 0):
        days = 366
    else:
       days = 365
    return days * 24


#map location unprocessed data
mapLocation = os.getcwd() + '\\data\\' + 'RADIUS' + RADIUS + 'KM'

#maplocation processed data
processedFilesLocation = os.getcwd() + '\\data\\RADIUS' +RADIUS + 'KM_PROCESSED'

# dEfine VALUES
YEARS = range(startYear, endYear+1)
missingValue = 999.9

#INITILIZE DICT
data_processed = {}
data_processed = dict.fromkeys(list(YEARS), {})

# load station ID current year
datalocationStationID= mapLocation +'\\STATION_ID.pickle'
file = open(datalocationStationID, 'rb')
currentUsableStations = pickle.load(file)

#make empty list to save the deleted stations
deletedStations = []

for year in YEARS:
    data_processed[year] = dict.fromkeys(list(currentUsableStations), {})
    
    print('PROCESSING YEAR: ', year,'...')
    
    # get path current year
    yearString = str(year)
    dataLocation = mapLocation + '\\' + yearString + '.pickle'

    # load data current year
    file = open(dataLocation, 'rb')
    data_year = pickle.load(file)
    
    # create range of dates
    base = datetime.datetime(year, 1, 1, 0, 0, tzinfo = pytz.UTC)
    numHours = get_number_of_hours_year(year)
    dateList = [base + datetime.timedelta(hours=x) for x in range(0, numHours)]
    
    #update station list to data with less then 3% missing data
    cut_off_percentage = 3     
    unusableStations = find_stations_unusable_temperatures(data_year, currentUsableStations, cut_off_percentage)
    
    for ID in unusableStations:
        print('Unusable Station: ', ID)
        index = currentUsableStations.index(ID)    
        currentUsableStations.pop(index) #deletes stations

    #remember which stations were deleted
    deletedStations +=unusableStations        
    
    # loop over stations
    for ID in currentUsableStations:
        
        print('Station: ', ID,':')
        
        # get keys from data
        currentKeys = list(data_year[ID].keys())
        data_processed[year][ID] = dict.fromkeys(currentKeys, [])
        
        #get datetime list from station
        datesMeasurement = data_year[ID]['datetime']
        indexMeasurement = []
        
        print('Matching dates...')
        for date in dateList:
            nearestDate = nearest(datesMeasurement, date)
            indexMeasurement.append(datesMeasurement.index(nearestDate))
        
        print('Storing values in new dictionary...')
        # store in new dictionary
        for key in currentKeys:
            
            if key == 'datetime':
                data_processed[year][ID][key] = dateList            
            else:
                data_processed[year][ID][key] = [ data_year[ID][key][index] for index in indexMeasurement ]

#Delete all unsusable stations from the list (as this is determined per year 
#there might be a station found unusable only later thus being present in earlier dictionaries)
print('Deleting all unsuable stations: ',deletedStations,'...')
for year in YEARS:
    for ID in deletedStations:
        dummy= data_processed[year].pop(ID,None)
    #have to assign dummy value otherwise deleted key gets printed
print('Saving dictionary...')
#SAVE DICTIONARIES
if not os.path.exists(processedFilesLocation):
    os.makedirs(processedFilesLocation)

with open(processedFilesLocation + '\\' + str(startYear) + '-' + str(endYear) + '.pickle', 'wb') as handle:
    pickle.dump(data_processed, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
with open(processedFilesLocation + '\\STATION_ID.pickle', 'wb') as handle:
     pickle.dump(currentUsableStations, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('PROCESSING COMPLETED')