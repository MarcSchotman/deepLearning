# -*- coding: utf-8 -*-
"""
Created on Mon May  7 22:02:59 2018

@author: m_a_s
"""


import numpy as np
import os.path
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

r_list = [100]

for r in r_list:
    stations = filter_stations(minStartDate, minEndDate, r, longitudeCenter, lattitudeCenter)
    
    #DATA GATEHRED: 
    keys = ['air_temperature','humidity','elevation','dew-point']#,'wind_speed','wind_direction','wind_observation_direction_type'
        
    # identifies what data to get
    YEARS = range(int(startYear), int(endYear))
    USAF_ID = stations['USAF']
    WBAN_ID = stations['WBAN']
    
    mapName = 'RADIUS' + str(r) +'KM'
    destinationPath = os.path.join('D:\\DUMMY\\',mapName)
    
    get_data(YEARS, USAF_ID,WBAN_ID,keys,destinationPath)