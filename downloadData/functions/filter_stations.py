# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:25:22 2018

@author: Marc & Taeke
"""


# does this give problems?
def filter_stations(minStartDate, minEndDate, r_max, longitudeCenter, lattitudeCenter):
    import numpy as np

    from functions_filter_stations import string_is_number, filter_station_date
    from functions_filter_stations import filter_station_radius, filter_station_activity, check_numbers, convert_number
    
    
    ## start of script
    isd_history_file = open('isd-history.txt', "r")
    isd_history1 = isd_history_file.read()
    isd_history = isd_history1.split("\n") #
    
    # clear text lines
    del(isd_history[0:22])
    
    #initilize dictionary
    stations ={}
    keys = ['USAF', 'WBAN', 'LAT', 'LON', 'ELEV', 'BEGIN', 'END']
    stations = stations.fromkeys(keys)
    #intilize dictionary as lists
    for key in keys:
                stations[key] = []
                
    for line in isd_history:
        lineNumeric = []
        #lineSplit = line.split()
        lineSplit = line.split()
        
        for item in lineSplit:
            if string_is_number(item):
                lineNumeric.append(item)
        
        if check_numbers(lineNumeric):  
            lineNumeric = convert_number(lineNumeric)
            
            for i in range(0,len(keys)):
                stations[keys[i]].append(lineNumeric[i])
    #longitude lattitude Delft, i.e. center of radius
    
    #        [ 0    1    2   3   4       5        6    ]  
    #stations = [USAF WBAN LAT LON ELEV BEGIN_DATE END_DATE]
    stations = filter_station_date(stations,keys,minStartDate,minEndDate)
    stations = filter_station_radius(stations,keys,longitudeCenter,lattitudeCenter,r_max)
    stations = filter_station_activity(stations,keys,minStartDate,minEndDate)
    
    return stations

