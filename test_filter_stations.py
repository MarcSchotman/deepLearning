# -*- coding: utf-8 -*-
"""
Created on Mon May 21 17:53:26 2018

@author: Taeke

Test filter stations
"""
from filter_stations import filter_stations
from plot_stations import plot_stations

# test function
# lattitudeCenter = 52.0116
# longitudeCenter = 4.3571       
lattitudeCenter = 39.7392
longitudeCenter = -104.9903
       
startDate = 20150101
endDate = 20170101
radius = 500

# filter stations
stations = filter_stations(startDate, endDate, radius, longitudeCenter, lattitudeCenter)

# plot result
plot_stations(stations, lattitudeCenter, longitudeCenter, radius)