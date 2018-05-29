# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:38:07 2018

@author: m_a_s
"""

import datetime
from data_mining import data_mining
from pre_processing import pre_processing
import os
import sys    
#location of functions
functionsLocation = os.path.join(os.getcwd(), 'functions')
sys.path.insert(0, functionsLocation)

from make_missingValueDict import make_missingValueDict

#INPUTS
lattitudeCenter = 39.7392 # Denver
longitudeCenter = -104.9903
startYear = 2017
endYear = 2018 #Will NOT download 2018
r_list = [100] #will downlaod for this list of radiuses making seperate dirs in deepLeanrning/data

#DOWNLOAD DATA
data_mining(startYear, endYear, r_list, lattitudeCenter, longitudeCenter)


#INPUTS
cut_off_percentage = 3 #ommits station with missing data > 3%
maxDiff = datetime.timedelta(.5) #Maximum difference between matched dates
missingValue = 999.9 # the key used for missing data
hoursADay = 24 #how many hours a day to we want to us

keys = ['datetime','air_temperature','sea_level_pressure','humidity','elevation','dew-point','wind_speed','wind_direction','wind_observation_direction_type','longitude','latitude']
filterKeys= ['air_temperature','sea_level_pressure','humidity','dew-point','wind_speed','wind_direction','wind_observation_direction_type']
missingValueList = make_missingValueDict()

#PREPROCESS DATA
for r in r_list:
    r = str(r)
    pre_processing(startYear, endYear, r, cut_off_percentage, maxDiff, missingValueList, filterKeys,hoursADay)


#map location unprocessed data
deepLearningPath, _  = os.path.split(os.getcwd())
RADIUS = 100
mapLocation = os.path.join(deepLearningPath, 'data', 'RADIUS' + str(RADIUS) + 'KM')

#maplocation processed data
processedFilesLocation = os.path.join(mapLocation, 'data', 'RADIUS' + str(RADIUS) + 'KM_PROCESSED')

year = 2017
#get path current year
yearString = str(year)
dataLocation = os.path.join(mapLocation, yearString + '.pickle')

import pickle
#load data current year
file = open(dataLocation, 'rb')
data_year = pickle.load(file)       

#x = [1,2,3,'MISSING']
#for element in x: 
#    if element == 'MISSING': 
#        print('yes')
#        
#x = [1,2,3,4,5]
#print(x.count(2))
