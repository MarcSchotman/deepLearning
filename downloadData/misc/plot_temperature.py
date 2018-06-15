# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018
@author: Taeke
"""

import matplotlib.pyplot as plt
import matplotlib #Type "%matplotlib qt"  in console to show figure in seperate window
import pickle
import os.path
import math
import numpy as np

#maplocation processed data
RADIUS = 100
missingValue = 999 # the key used for missing data

processedFilesLocation = os.path.join(os.getcwd(), '..\..\data', 'RADIUS' + str(RADIUS) + 'KM_PROCESSED')
imageName = os.path.join('..', '..', 'fig', 'temperature')

dataLocation = processedFilesLocation + '/' + '2017.pickle'
file = open(dataLocation, 'rb')
data = pickle.load(file)

datalocationStationID= processedFilesLocation +'\STATION_ID.pickle'
file = open(datalocationStationID, 'rb')
stationIDs = pickle.load(file)

numberOfStations = len(stationIDs)
# 'wind_north' wind_speed  wind_direction
keys = ['wind_speed', 'datetime']

useless = []
# for the third station we first 40% of the data is currupted, however 
# somewhere around index 18000 the date seems to reset back to 2017-01-01 and 
# from then on we have proper data. Why is the time not constantly increasing?
plot_number = math.ceil(numberOfStations/3)
pltcount = 1
count =0 
plt.figure(figsize = (20,10))
for ID in stationIDs:
    print('Station number '+ str(count) + ', with ID: ' + str(ID))
    # extract data
    temperature = np.array(data[ID]['wind_east'])
    date = np.array(data[ID]['datetime'])
    
    dateNumeric = matplotlib.dates.date2num(date)
    # determine wehter station is useless
    
    missingData = sum(temperature == missingValue)
    if missingData == len(temperature):
        useless.append(ID)
        print(' is useless')
    else: 
        
        print(str(round(missingData/len(temperature) * 100,2)) + '% of data missing: ' + str(missingData) +  ' data points' )
        temperature[temperature == missingValue] = math.nan
        plt.subplot(plot_number,3,pltcount)
        plt.plot(date, temperature, label = ID)
        plt.legend()
#        plt.ylabel('Temperatre [C]')
#        plt.xlabel('Data Sample')
        #plt.plot(dateNumeric, label = ID)
        pltcount += 1
    count +=1
plt.show()
plt.savefig(imageName + '.eps', bbox_inches='tight')