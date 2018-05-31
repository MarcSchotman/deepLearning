# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018

@author: Taeke
"""

def filter_on_missing_values(data, stationIDs,key, missingValue,filterKeys, cut_off_percentage):
    import numpy as np
    #initilize array
    unUseableStations = []
    for ID in stationIDs:
        #get temperature and missing percentage
        stationData = data[ID][key]
        missingData = stationData.count(missingValue)
        percentage_missing = (missingData/len(stationData))*100
        
        if (key in filterKeys) and percentage_missing> cut_off_percentage: 
            print('Unusable Station: ', ID, 'percentage of ',key,' missing: ', round(percentage_missing,2), '%')
            unUseableStations.append(ID)
        
        
    
    return unUseableStations