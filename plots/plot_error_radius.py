# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:03:16 2018

@author: Taeke
"""

import csv
import os
import numpy as np
import matplotlib.pyplot as plt


radius = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
network = 'm2m_lstm'
feature = ['air_temperature', 'humidity']
feature = ['air_temperature']
path = os.path.join('..', 'out', '_'.join(feature))
fileID = 'log.csv'

finalError = [0] * len(radius)
rCounter = 0
# loop over radii
for r in radius:
    filePath = os.path.join(path, network + '_' + str(r) + '_'.join(feature), fileID)
    with open(filePath) as csvfile:
        file = csv.reader(csvfile, delimiter=',')
    
        # init new numpy array
        data = [[]]
        for row in file:

            # convert to numeric value
            try:
                row = [[float(i) for i in row]]
                if not any(data[0]):
                    data = row
                else:
                    data = np.append(data, row, axis=0)
            except ValueError:
                print("Not a float")
    
    finalError[rCounter] = data[-1, -1]
    
    rCounter = rCounter + 1
    
    
fig, ax = plt.subplots( nrows=1, ncols=1 ) 
ax.plot(radius, finalError)
plt.ylabel('Mean squared error expressed in stds')
plt.xlabel('radius [km]')
plt.grid(True)
plt.title(' '.join(feature))

fig.savefig(os.path.join('..', 'fig', 'error_' + '_'.join(feature) + '.png'))


plt.close(fig) 