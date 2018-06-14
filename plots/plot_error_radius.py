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
                print("Not a float")
    return data

## set properties
radius = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
network = 'm2m_lstm'
feature = ['air_temperature', 'humidity']
feature = ['air_temperature']

# set path
path = os.path.join('..', 'out2')
dataFileID = 'log.csv'
dataStatFileId = 'data_stat.txt'

# init some stuff for looping
RMS = [0] * len(radius)
RMS_norm = [0] * len(radius)
rCounter = 0

# loop over radii
for r in radius:
    
    # init path
    fullPath = os.path.join(path, network + '_'.join(feature), str(r))
    dataFilePath = os.path.join(fullPath, dataFileID)
    dataStatPath = os.path.join(fullPath, dataStatFileId)

    data = read_numeric(dataFilePath)
    dataStat = read_numeric(dataStatPath)

    RMS_norm[rCounter] = data[-1, -1]
    RMS[rCounter] = dataStat[2] * dataStat[2] * data[-1, -1]

    rCounter = rCounter + 1

# plot results
fig, ax = plt.subplots( nrows=1, ncols=1 ) 
ax.plot(radius, RMS)
plt.ylabel('Mean squared error expressed in stds')
plt.xlabel('radius [km]')
plt.grid(True)
plt.title(' '.join(feature))

fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.png'))


plt.close(fig) 