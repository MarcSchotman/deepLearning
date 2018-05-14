# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:52:27 2018

@author: Taeke
"""

import matplotlib.pyplot as plt
import matplotlib
import pickle
import os
import math
import numpy as np

dataLocation = os.getcwd() + '\\data\\RADIUS100KM\\2017.pickle'

file = open(dataLocation, 'rb')

data = pickle.load(file)

stationIDs = list(data.keys())
numberOfStations = len(stationIDs)

keys = ['air_temperature', 'datetime']

useless = []
count = 0

# for the third station we first 40% of the data is currupted, however 
# somewhere around index 18000 the date seems to reset back to 2017-01-01 and 
# from then on we have proper data. Why is the time not constantly increasing?
for ID in stationIDs[0:3]:
    print('Station number '+ str(count) + ', with ID: ' + str(ID))
    # extract data
    temperature = np.array(data[ID]['air_temperature'])
    date = np.array(data[ID]['datetime'])
    
    dateNumeric = matplotlib.dates.date2num(date)
    # determine wehter station is useless
    
    missingData = sum(temperature > 500)
    if missingData == len(temperature):
        useless.append(ID)
        print(' is useless')
    else: 
        
        print(' missing data: '+ str(missingData) +  ', which is: ' + str(missingData/len(temperature) * 100) + '%')
        # temperature[temperature > 500] = math.nan
        plt.plot(date, temperature, label = ID)
        plt.plot(dateNumeric, label = ID)
    
    count = count + 1
    
plt.legend()

plt.ylabel('Temperatre [C]')
plt.xlabel('Data Sample')

plt.grid(True)
plt.show()