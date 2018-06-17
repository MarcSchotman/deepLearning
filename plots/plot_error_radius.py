# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:03:16 2018

@author: Taeke
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def read_numeric(dataFilePath):
    import csv
    
    with open(dataFilePath) as csvfile:
        dataFile = csv.reader(csvfile, delimiter=',')
        # init new numpy array
        data = [[]]
        for row in dataFile:
        
            # convert to numeric value
            try:
                row = [[float(i) for i in row]]
                if not any(data[0]):
                    data = row
                else:
                    data = np.append(data, row, axis=0)
            except ValueError:
                print('skip line' + row[1])
    return data

## set properties
radius = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
network = 'm2m_lstm'
# feature = ['air_temperature', 'humidity']
# feature = ['air_temperature']
features =  [['air_temperature'], ['air_temperature', 'wind_north', 'wind_east']]

# set path
path = os.path.join('..', 'out')
dataFileID = 'log.csv'
dataStatFileId = 'data_stat.csv'

# init some stuff for looping
RMS = [[0]  * len(radius), [0]  * len(radius)]
RMS_norm = [[0]  * len(radius), [0]  * len(radius)]


featCounter = 0

for feature in features:
    
    rCounter = 0
    # loop over radii
    for r in radius:
        
        # init path
        fullPath = os.path.join(path, network + '_'.join(feature), str(r))
        dataFilePath = os.path.join(fullPath, dataFileID)
        dataStatPath = os.path.join(fullPath, dataStatFileId)
    
        data = read_numeric(dataFilePath)
        dataStat = read_numeric(dataStatPath)
        
        print( data[-1, -1])
    
        RMS_norm[featCounter][rCounter] = data[-1, -1]
        RMS[featCounter][rCounter] = dataStat[0][1] * dataStat[0][1] * data[-1, -1]
    
        rCounter = rCounter + 1
        
    featCounter = featCounter + 1
# plot results
fig, ax = plt.subplots( nrows=1, ncols=1 ) 
tempPlt, = ax.plot(radius, RMS[0], label='temperature')
windPlt, = ax.plot(radius, RMS[1], label='temperatur, wind speed')
plt.ylabel('Mean squared error [$^\circ$ C$^2$]')
plt.xlabel('radius [km]')
plt.grid(True)
plt.title('Error for Different Features and Radii')

handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=[tempPlt, windPlt])

fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.png'))
fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.eps'))

plt.show(fig) 
# plt.close(fig) 