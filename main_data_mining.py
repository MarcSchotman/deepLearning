# -*- coding: utf-8 -*-
"""
Created on Mon May  7 22:02:59 2018

@author: m_a_s
"""
#import function
import numpy as np
import os.path
import pickle
from filter_stations import filter_stations
from get_data import get_data
import os # To get the current working directory use
#lattitude and longitude Delft
lattitudeCenter = 52.0116
longitudeCenter = 4.3571
startYear = '2017'
endYear = '2018'
r_list = [50, 100, 110]

minStartDate = int(startYear+'0000') #YearMonthDay
minEndDate = int(endYear+'0000')  #YearMonthDay
map_location = 'D:\\DATA_NEW'
map_location = os.getcwd() + '\data'
# cwd = os.getcwd()

#DATA GATEHRED: 
keys = ['datetime','air_temperature','humidity','elevation','dew-point','wind_speed','wind_direction','wind_observation_direction_type']

for r in r_list:
    print('RADIUS: ', r, ' KM')
    stations = filter_stations(minStartDate, minEndDate, r, longitudeCenter, lattitudeCenter)
        
    # identifies what data to get
    YEARS = range(int(startYear), int(endYear))
    
    USAF_ID = list(stations['USAF'])
    WBAN_ID = list(stations['WBAN'])
    STATION_ID = [USAF_ID, WBAN_ID]
    
    mapName = 'RADIUS' + str(r) +'KM'
    destinationPath = os.path.join(map_location,mapName)
    
    if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)
        
    #uses pikcle for dumping dictionary containg station ID's
    with open(destinationPath +'\\STATION_ID' + '.pickle', 'wb') as handle:
        pickle.dump(STATION_ID, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #check which stations have already been downloaded previously
    current_index_r = r_list.index(r)
    removed_stations = []
    if current_index_r != 0:
        prev_mapName='RADIUS' +str(r_list[current_index_r -1]) + 'KM'
        previous_path = os.path.join(map_location,prev_mapName)        
        
        with open(previous_path+'\\STATION_ID' + '.pickle','rb') as handle:
            prev_STATION_ID_LIST = pickle.load(handle)
            prev_USAF = prev_STATION_ID_LIST[0]
            prev_WBAN = prev_STATION_ID_LIST[1]
    
        #remove the already downloaded ID's from the 'to download list'      
        for index in range(0,len(prev_USAF)):
            
            if prev_USAF[index] in USAF_ID:
                index_match = USAF_ID.index(prev_USAF[index])
                #if at the same idnex also the other ID matches THEN remove them from the list
                if prev_WBAN[index] == WBAN_ID[index_match]:
                    USAF_ID.remove(prev_USAF[index])
                    WBAN_ID.remove(prev_WBAN[index])
                    removed_stations.append([prev_USAF[index], prev_WBAN[index]])
    print('Stations to download:',len(USAF_ID))              
    print('Stations already downloaded:',len(removed_stations))
    #downloads all data for all stations in station_ID and years in year
    for year in YEARS:
        try:
            data_year = get_data(year, USAF_ID,WBAN_ID,keys,destinationPath)
        except Exception as ex:
            print('ERROR:', ex)
            print('trying again...')
            try:
                data_year = get_data(year, USAF_ID,WBAN_ID,keys,destinationPath)
            except Exception as ex:
                print('ERROR: ',ex)
                print('STOPPING DOWNLOAD.')
        
        #add previously downloaded data to the current data_year
        if current_index_r != 0:        
            with open(previous_path+'\\' + str(year)+ '.pickle','rb') as handle:
                prev_data_year = pickle.load(handle)
                
            for index in range(0,len(removed_stations)):
                station_id = removed_stations[index][0] + '-' + removed_stations[index][1]
                data_year[station_id] = []
                data_year[station_id] = prev_data_year[station_id].copy()
        print('Total stations being saved:',len(data_year))    
        
        #time to save the dict
        file_name = str(year)
        full_path_name = os.path.join(destinationPath,file_name)
        
        if not os.path.exists(destinationPath):
                os.makedirs(destinationPath)
                
        #uses pikcle for dumping dictionary
        with open(full_path_name + '.pickle', 'wb') as handle:
            pickle.dump(data_year, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Download completed')