# -*- coding: utf-8 -*-
"""
Created on Tue May 29 10:58:02 2018

@author: Taeke
"""

import pickle

RADIUS = 200
year = 2017
import os.path

#map location unprocessed data
deepLearningPath, _  = os.path.split(os.getcwd())
mapLocation = os.path.join(deepLearningPath, 'data', 'RADIUS' + str(RADIUS) + 'KM')

#maplocation processed data
processedFilesLocation = os.path.join(os.getcwd(), 'data', 'RADIUS' + str(RADIUS) + 'KM_PROCESSED')


# data_processed = {}
# data_processed = dict.fromkeys(list(usableStations), {})

print('PROCESSED YEAR: ', year,'...')

#get path current year
yearString = str(year)
dataLocation = os.path.join(mapLocation, yearString + '.pickle')

#load data current year
file = open(dataLocation, 'rb')
data_year = pickle.load(file)   