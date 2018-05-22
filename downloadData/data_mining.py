# -*- coding: utf-8 -*-
"""
Created on Mon May  7 22:02:59 2018

@author: m_a_s
"""

#INPUTS
lattitudeCenter = 39.7392 #lattitude and longitude Delft
longitudeCenter = -104.9903
startYear = '2015'
endYear = '2018' #Will NOT download 2018
r_list = [200] #will downlaod for this list of radiuses making seperate dirs in deepLeanrning/data


#import functions
import numpy as np
import os
import pickle
import sys

#location of functions
functionsLocation = os.path.join(os.getcwd(), 'functions')
sys.path.insert(0, functionsLocation)

from filter_stations import filter_stations
from get_data import get_data


minStartDate = int(startYear+'0000') #YearMonthDay
minEndDate = int(endYear+'0000')  #YearMonthDay
map_location = os.path.join(os.getcwd() , 'data')

#DATA GATEHRED: 
keys = ['datetime','air_temperature','sea_level_pressure','humidity','elevation','dew-point','wind_speed','wind_direction','wind_observation_direction_type','longitude','latitude']

for r in r_list:
    print('RADIUS: ', r, ' KM')
    stations = filter_stations(minStartDate, minEndDate, r, longitudeCenter, lattitudeCenter)
    # identifies what data to get
    YEARS = range(int(startYear), int(endYear))
    
    USAF_ID = list(stations['USAF'])
    WBAN_ID = list(stations['WBAN'])
   #concatenates the two ID's with '-' in between
    STATION_ID_LIST=["{}-{:2}".format(a_, b_) for a_, b_ in zip(USAF_ID, WBAN_ID)]
    
    mapName = 'RADIUS' + str(r) +'KM'
    destinationPath = os.path.join(map_location,mapName)
    
    if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)
        
    #uses pikcle for dumping dictionary containg station ID's
    pathStationID = os.path.join(destinationPath,'STATION_ID.pickle')
    with open(pathStationID, 'wb') as handle:
        pickle.dump(STATION_ID_LIST, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #check which stations have already been downloaded previously
    current_index_r = r_list.index(r)
    removed_stations = []
    if current_index_r != 0:
        prev_mapName='RADIUS' +str(r_list[current_index_r -1]) + 'KM'
        previous_path = os.path.join(map_location,prev_mapName)        
        previousPathStations = os.path.join(previous_path,'STATION_ID.pickle')
        
        with open(previousPathStations,'rb') as handle:
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
        #Attemps three times to download data before stopping
        try:
            data_year = get_data(year, STATION_ID_LIST,keys,destinationPath)
        except Exception as ex:
            print('ERROR:', ex)
            print('trying again...')
            try:
                data_year = get_data(year, STATION_ID_LIST, keys,destinationPath)
            except Exception as ex:
                print('ERROR: ',ex)
                print('trying again (second time)...')
                try:
                    data_year = get_data(year, STATION_ID_LIST, keys,destinationPath)
                except Exception as ex:
                    print('ERROR: ',ex)
                    print('STOPPING DOWNLOAD.')
        
        #add previously downloaded data to the current data_year
        if current_index_r != 0:
            fileName = str(year) + '.pickle'
            previousPathData = os.path.join(previous_path , fileName)
            with open(previousPathData,'rb') as handle:
                prev_data_year = pickle.load(handle)
                
            for index in range(0,len(removed_stations)):
                station_id = removed_stations[index][0] + '-' + removed_stations[index][1]
                data_year[station_id] = []
                data_year[station_id] = prev_data_year[station_id].copy()
        print('Total stations being saved:',len(data_year))    
        
        #time to save the dict
        fileName = str(year) +'.pickle'
        full_path_name = os.path.join(destinationPath,fileName)
        
        if not os.path.exists(destinationPath):
                os.makedirs(destinationPath)
                
        #uses pikcle for dumping dictionary
        with open(full_path_name, 'wb') as handle:
            pickle.dump(data_year, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Download completed')