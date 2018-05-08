# -*- coding: utf-8 -*-
"""
Created on Mon May  7 22:02:59 2018

@author: m_a_s
"""


import numpy as np
import os.path
import pickle
#import function
from filter_stations import filter_stations
from get_data import get_data

#lattitude and longitude Delft
lattitudeCenter = 52.0116
longitudeCenter = 4.3571
startYear = '2017'
endYear = '2018'

minStartDate = int(startYear+'0000') #YearMonthDay
minEndDate = int(endYear+'0000')  #YearMonthDay

r_list = [50]

for r in r_list:
    stations = filter_stations(minStartDate, minEndDate, r, longitudeCenter, lattitudeCenter)
    
    
    #DATA GATEHRED: 
    keys = ['datetime','air_temperature','humidity','elevation','dew-point']#,'wind_speed','wind_direction','wind_observation_direction_type'
        
    # identifies what data to get
    YEARS = range(int(startYear), int(endYear))
    
    USAF_ID = stations['USAF']
    WBAN_ID = stations['WBAN']
    STATION_ID = [USAF_ID, WBAN_ID]
    
    mapName = 'RADIUS' + str(r) +'KM'
    destinationPath = os.path.join('C:\\Users\\m_a_s\\Documents\\DUMMYDATA',mapName)
    if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)
        
    #uses pikcle for dumping dictionary containg station ID's
    with open(destinationPath +'\\STATION_ID' + '.pickle', 'wb') as handle:
        pickle.dump(STATION_ID, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #downloads all data for all stations in station_ID and years in year
    get_data(YEARS, USAF_ID,WBAN_ID,keys,destinationPath)