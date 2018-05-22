# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:38:34 2018

@author: m_a_s
"""
def find_usable_stations(YEARS,mapLocation, maxDiff, missingValue,cut_off_percentage):
    
    import pickle
    from get_number_of_hours_year import get_number_of_hours_year
    from find_stations_unusable_temperatures import find_stations_unusable_temperatures
    import datetime
    import os.path
    from match_dates import match_dates
    import pytz
    
    datalocationStationID= os.path.join(mapLocation, 'STATION_ID.pickle')
    file = open(datalocationStationID, 'rb')
    currentUsableStations = pickle.load(file)

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
    return currentUsableStations            