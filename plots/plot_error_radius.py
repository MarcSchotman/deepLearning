# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:03:16 2018

@author: Taeke
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import math as mth

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
                print('skip line')
    return data

## set properties
radius = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
network = 'm2m_lstm'
# feature = ['air_temperature', 'humidity']
# feature = ['air_temperature']
features =  [['air_temperature'], ['air_temperature', 'wind_north', 'wind_east'], ['air_temperature', 'humidity']]

# set path
path = os.path.join('..', 'out')
dataFileID = 'log.csv'
dataStatFileId = 'data_stat.csv'

radiusS = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
radiusL = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

# init some stuff for looping
RMS = [[0]  * len(radiusL), [0]  * len(radiusL), [0]  * len(radiusS)]
RMSnorm = [[0]  * len(radiusL), [0]  * len(radiusL), [0]  * len(radiusS)]

RMSTrain = [[0]  * len(radiusL), [0]  * len(radiusL), [0]  * len(radiusS)]
RMSnormTrain = [[0]  * len(radiusL), [0]  * len(radiusL), [0]  * len(radiusS)]

featCounter = 0

for feature in features:
    
    if featCounter == 2:
        radius = radiusS
    else:
        radius = radiusL
    
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
    
        RMSnorm[featCounter][rCounter] = mth.sqrt(data[-1, 2])
        RMS[featCounter][rCounter] = mth.sqrt(dataStat[0][1] * dataStat[0][1] * data[-1, 2])
        
        RMSnormTrain[featCounter][rCounter] = mth.sqrt(data[-1, 1])
        RMSTrain[featCounter][rCounter] = mth.sqrt(dataStat[0][1] * dataStat[0][1] * data[-1, 1])
        
        rCounter = rCounter + 1
        
    featCounter = featCounter + 1


csfont = {'fontname':'Century Gothic'}

valStyle = '-'
trainStyle = '--'

r = [245/255, 159/255,35/2555] # given by Marc
b = [102/255, 161/255, 211/255] # given by Marc
lineWidth = 2.5

# plot results   
fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(10, 6) ) 
plt.subplots_adjust(top=0.77)


tempPlt, = ax.plot(radiusL, RMS[0], label='temperature, validate',  color=b, linestyle = valStyle, linewidth = lineWidth)
windPlt, = ax.plot(radiusL, RMS[1], label='temperature + wind speed, validate',  color=r, linestyle = valStyle, linewidth = lineWidth)
humidPlt, = ax.plot(radiusS, RMS[2], label='temperature + humidity, validate',  color='g', linestyle = valStyle, linewidth = lineWidth)

tempPltTrn, = ax.plot(radiusL, RMSTrain[0], label='temperature, train' ,color=b, linestyle = trainStyle, linewidth = lineWidth)
windPltTrn, = ax.plot(radiusL, RMSTrain[1], label='temperature + wind speed, train', color=r, linestyle = trainStyle, linewidth = lineWidth)
humidPltTrn, = ax.plot(radiusS, RMSTrain[2], label='temperature + humidity, train', color='g', linestyle = trainStyle, linewidth = lineWidth)

plt.ylabel('root mean squared error [$^\circ$C]', fontsize=16, **csfont)
plt.xlabel('radius [km]', fontsize=16, **csfont)
plt.grid(True)
plt.title('Error for Different Features and Radii', fontsize=20, **csfont , y=1.1)

ax.set_xticklabels(ax.get_xticks(), fontsize=14, **csfont)
ax.set_yticklabels(ax.get_yticks(), fontsize=14, **csfont)

handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=[tempPlt, windPlt, humidPlt, tempPltTrn, windPltTrn, humidPltTrn], 
           prop={'family': 'Century Gothic', 'size'   : 13}, 
           bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

plt.xlim(xmin = 100, xmax=1200)
plt.ylim(ymin = 3, ymax=12)

fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.png'))
fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.eps'))

plt.show(fig) 