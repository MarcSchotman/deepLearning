# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:42:28 2018

@author: m_a_s
"""
a = [['1','2'],['3','4']]
b = ['1','3']

if not (b in a):
    print('no')

#INPUTS
lattitudeCenter = 39.74
longitudeCenter = -104.99
startYear = 2015
endYear = 2018 #Will NOT download 2018
r_max = 200 #will downlaod for this list of radiuses making seperate dirs in deepLeanrning/data

import os
import sys
#location of functions
functionsLocation = os.path.join(os.getcwd(), 'functions')
sys.path.insert(0, functionsLocation)
    
from filter_stations import filter_stations

startYear = str(startYear)
endYear = str(endYear)

minStartDate = int(startYear+'0000') #YearMonthDay
minEndDate = int(endYear+'0000')  #YearMonthDay

stations = filter_stations(minStartDate, minEndDate, r_max, longitudeCenter, lattitudeCenter)