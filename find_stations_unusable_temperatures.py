# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018

@author: Taeke
"""

def find_stations_unusable_temperatures(data, stationIDs, cut_off_percentage):
    import numpy as np
    #initilize array
    unUseableStations = []
    for ID in stationIDs:
        #get temperature and missing percentage
        temperature = np.array(data[ID]['air_temperature'])       
        missingData = sum(temperature ==999.9)
        percentage_missing = (missingData/len(temperature))*100
        
        if percentage_missing> cut_off_percentage: 
            unUseableStations.append(ID)
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
