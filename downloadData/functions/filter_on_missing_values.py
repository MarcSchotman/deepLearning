# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018

@author: Taeke
"""

def filter_on_missing_values(data, stationIDs,key,missingValue, cut_off_percentage):
    import numpy as np
    #initilize array
    unUseableStations = []
    for ID in stationIDs:
        #get temperature and missing percentage
        stationData = data[ID][key]
        missingData = stationData.count(missingValue)
        percentage_missing = (missingData/len(stationData))*100
        
        if key == 'air_temperature' and percentage_missing> cut_off_percentage: 
            print('Unusable Station: ', ID, 'percentage of data missing: ', percentage_missing, '%')
            unUseableStations.append(ID)
        
    print(round(percentage_missing,2), '% missing of ' ,key,'...ONLY AIR_TEMPERATURE IS USED TO FILTER' )
        
    
    return unUseableStations