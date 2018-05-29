# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018

@author: Taeke
"""

def filter_on_missing_values(data, stationIDs,key,missingValue, cut_off_percentage):
    import numpy as np
    #initilize array
    unUseableStations = []
    print('Filtering: ', key)
    for ID in stationIDs:
        #get temperature and missing percentage
        stationData = data[ID][key]
        print(len(stationData))
        missingData = stationData.count(missingValue)
        percentage_missing = (missingData/len(stationData))*100
        
        if key == 'air_temperature' and percentage_missing> cut_off_percentage: 
            print('Unusable Station: ', ID, 'percentage of data missing: ', percentage_missing, '%')
            unUseableStations.append(ID)
        
    print('Now at key: ', key, '. Missing percentage: ' , round(percentage_missing,2) )
        
    
    return unUseableStations

#import pickle
##dataLocation = os.getcwd() + '\\data\\RADIUS40KM\\2017.pickle'
#mapLocation = 'C:\\Users\\m_a_s\\Desktop\\data\\RADIUS50KM'
#
#dataLocation = mapLocation + '\\2017.pickle'
#file = open(dataLocation, 'rb')
#data = pickle.load(file)
#
#datalocationStationID= mapLocation +'\\STATION_ID.pickle'
#file = open(datalocationStationID, 'rb')
#stationIDs = pickle.load(file)
#
#useableStations = find_stations_useable_temperatures(data,stationIDs,2)
#print(useableStations)
