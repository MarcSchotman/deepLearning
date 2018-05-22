# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:37:28 2018

@author: Taeke
"""

import datetime

#INPUTS
startYear = 2017
endYear = 2018 #downloads UPTILL endyear so NOT 2018
RADIUS = '100' #ASSSUMES DATA IN /deepLearning/data
cut_off_percentage = 3 #ommits station with missing data > 3%
maxDiff = datetime.timedelta(.5) #Maximum difference between matched dates

import numpy as np
import pickle
import os.path

import pytz
from find_stations_unusable_temperatures import find_stations_unusable_temperatures
import time



def match_dates(dateList, data_year, currentKeys, ID, maxDiff, missingValue):
    #checks dates and fills in missing value if date difference is larger then  maxDiff
    
    index = 1 #NEEDS TO BE 1
    datesStation = data_year[ID]['datetime']
    outList = {}
    outList = dict.fromkeys(currentKeys)
    for key in currentKeys:
        outList[key] = []
    
    
    for date in dateList:
        match = False
        last_delta = abs(date - datesStation[index-1])
        
        while match==False:
            delta = abs(date - datesStation[index])
            if delta > last_delta:
                match =True
                #makes sure that when at the last index it stays there i.e. not index+=1
            elif (index) == len(datesStation)-1:
                match =True
            else:
                #only continue if there was no match
                index +=1    
                last_delta = delta
        
        if last_delta > maxDiff:
            missing = True
        else:
            missing = False
            
        for key in currentKeys:
            if key == 'datetime':
                outList[key] = dateList
            elif missing:
                outList[key].append(missingValue)
            else:                    
                outList[key].append(data_year[ID][key][index])

    return outList
        
def get_number_of_hours_year(year): 
    if (year % 4) == 0 and (year % 100 != 0 or year % 400 == 0):
        days = 366
    else:
       days = 365
    return days * 24
    
#map location unprocessed data
mapLocation = os.path.join(os.getcwd(), 'data', 'RADIUS' + str(RADIUS) + 'KM')

#maplocation processed data
processedFilesLocation = os.path.join(os.getcwd(), 'data', 'RADIUS' + str(RADIUS) + 'KM_PROCESSED')

# define VALUES
YEARS = range(startYear, endYear)
missingValue = 999.9 # the key used for missing data

# load station ID current year
datalocationStationID= os.path.join(mapLocation, 'STATION_ID.pickle')
file = open(datalocationStationID, 'rb')
currentUsableStations = pickle.load(file)

tic = time.clock()
#Determine which stations are usable during entire period i.e. check missing percentage < cut off percentage
for year in YEARS:
    print('Determining useless stations for year: ', year)
    
    # get path current year
    yearString = str(year)
    dataLocation = os.path.join(mapLocation, yearString + '.pickle')

    # load data current year
    file = open(dataLocation, 'rb')
    data_year = pickle.load(file)
    
    #first check dates then check misding percentage
    #create range of dates
    base = datetime.datetime(year, 1, 1, 0, 0, tzinfo = pytz.UTC)
    numHours = get_number_of_hours_year(year)
    dateList = [base + datetime.timedelta(hours=x) for x in range(0, numHours)]      
    
    for ID in currentUsableStations:
        currentKeys = list(data_year[ID].keys())
        data_year[ID] = match_dates(dateList, data_year, currentKeys, ID, maxDiff, missingValue)
        
    unusableStations = find_stations_unusable_temperatures(data_year, currentUsableStations, cut_off_percentage)
    
    for ID in unusableStations:
        index = currentUsableStations.index(ID)    
        currentUsableStations.pop(index) #deletes stations
  #use these stations for preprocessing  
usableStations = currentUsableStations

toc = time.clock()
print(round(toc-tic,2),'s: filtered stations')

for year in YEARS:
    data_processed = {}
    data_processed = dict.fromkeys(list(usableStations), {})
    
    print('YEAR: ', year,'...')
    
    #get path current year
    yearString = str(year)
    dataLocation = os.path.join(mapLocation, yearString + '.pickle')

    #load data current year
    file = open(dataLocation, 'rb')
    data_year = pickle.load(file)
    
    #create range of dates
    base = datetime.datetime(year, 1, 1, 0, 0, tzinfo = pytz.UTC)
    numHours = get_number_of_hours_year(year)
    dateList = [base + datetime.timedelta(hours=x) for x in range(0, numHours)]        
    
    #loop over stations
    for ID in usableStations:
        # get keys from data
        currentKeys = list(data_year[ID].keys())
        data_processed[ID] = dict.fromkeys(currentKeys, [])
        #get datetime list from station
  
        tic = time.clock()
        data_processed[ID]= match_dates(dateList, data_year, currentKeys, ID, maxDiff, missingValue)
        toc = time.clock()
        #have to assign dummy value otherwise deleted key gets printed
    #SAVE DICTIONARIES
    if not os.path.exists(processedFilesLocation):
        os.makedirs(processedFilesLocation)
    
    with open(os.path.join(processedFilesLocation, str(year) + '.pickle'), 'wb') as handle:
        pickle.dump(data_processed, handle, protocol=pickle.HIGHEST_PROTOCOL)
#save station ID list          
with open(os.path.join(processedFilesLocation, 'STATION_ID.pickle'), 'wb') as handle:
    pickle.dump(usableStations, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('PROCESSING COMPLETED')  