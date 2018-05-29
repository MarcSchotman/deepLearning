# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:37:28 2018

@author: Taeke
"""
import datetime


def pre_processing(startYear, endYear, RADIUS, cut_off_percentage, maxDiff, missingValueList, filterKeys,hoursADay):
    import numpy as np
    import pickle
    import os.path
    import sys
    
    #location of functions
    functionsLocation = os.path.join(os.getcwd(), 'functions')
    sys.path.insert(0, functionsLocation)
    
    from find_usable_stations import find_usable_stations
    from match_dates import match_dates
    from desired_date_list import desired_date_list
    
    
    #map location unprocessed data
    deepLearningPath, _  = os.path.split(os.getcwd())
    mapLocation = os.path.join(deepLearningPath, 'data', 'RADIUS' + str(RADIUS) + 'KM')
    
    #maplocation processed data
    processedFilesLocation = os.path.join(mapLocation, 'data', 'RADIUS' + str(RADIUS) + 'KM_PROCESSED')
    
    # define VALUES
    YEARS = range(startYear, endYear)
    
    #Determine which stations are usable during entire period i.e. check missing percentage < cut off percentage
    #use these stations for preprocessing  

    usableStations = find_usable_stations(YEARS,mapLocation, hoursADay, maxDiff, missingValueList, filterKeys,cut_off_percentage)
    
    #puts all the data of the usable stations in the desired format, i.e. hourly for 365 days a year.
    for year in YEARS:
        data_processed = {}
        data_processed = dict.fromkeys(list(usableStations), {})
        
        print('PROCESSED YEAR: ', year,'...')
        
        #get path current year
        yearString = str(year)
        dataLocation = os.path.join(mapLocation, yearString + '.pickle')
        
        #load data current year
        file = open(dataLocation, 'rb')
        data_year = pickle.load(file)            
        
        #loop over stations
        for ID in usableStations:
            # get keys from data
            currentKeys = list(data_year[ID].keys())
            data_processed[ID] = dict.fromkeys(currentKeys, [])
            
            #get desired dateList
            dateList = desired_date_list(year, hoursADay)
      
            data_processed[ID]= match_dates(dateList, data_year, currentKeys, ID, maxDiff, missingValueList)
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
    return 0

#import datetime
##INPUTS
#startYear = 2017
#endYear = 2018 #downloads UPTILL endyear so NOT 2018
#RADIUS = '100' #ASSSUMES DATA IN /deepLearning/data
#cut_off_percentage = 3 #ommits station with missing data > 3%
#maxDiff = datetime.timedelta(.5) #Maximum difference between matched dates
#missingValue = 999.9 # the key used for missing data
#hoursADay = 24 #how many hours a day to we want to us
#
#pre_processing(startYear, endYear, RADIUS, cut_off_percentage, maxDiff, missingValue,hoursADay)