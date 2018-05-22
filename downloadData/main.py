# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:38:07 2018

@author: m_a_s
"""

import datetime
from data_mining import data_mining
from pre_processing import pre_processing


#INPUTS
lattitudeCenter = 52.0116 #lattitude and longitude Delft
longitudeCenter = 4.3571
startYear = 2017
endYear = 2018 #Will NOT download 2018
r_list = [50] #will downlaod for this list of radiuses making seperate dirs in deepLeanrning/data

#DOWNLOAD DATA
#data_mining(startYear, endYear, r_list, lattitudeCenter, longitudeCenter)


#INPUTS
cut_off_percentage = 3 #ommits station with missing data > 3%
maxDiff = datetime.timedelta(.5) #Maximum difference between matched dates
missingValue = 999.9 # the key used for missing data
hoursADay = 24 #how many hours a day to we want to us

#PREPROCESS DATA
for r in r_list:
    r = str(r)
    pre_processing(startYear, endYear, r, cut_off_percentage, maxDiff, missingValue,hoursADay)