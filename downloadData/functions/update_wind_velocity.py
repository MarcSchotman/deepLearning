# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:52:14 2018

@author: Taeke
"""
import numpy as np

def update_wind_velocity(data, generalMissingValue, missingValueList):

    
    
    # The rate of horizontal travel of air past a fixed point in meters per second
    windSpeed = np.array(data['wind_speed'])
    
    # The angle, measured in a clockwise direction, between true north and 
    # the direction from which the wind is blowing.
    # MIN: 001 MAX: 360 UNITS: Angular Degrees
    windDir = np.radians(np.array(data['wind_direction']))
    
    
    data['wind_north'] = (-np.cos(windDir) * windSpeed).tolist()
    data['wind_east'] = (-np.sin(windDir) * windSpeed).tolist()


    # where we have a missing value for wind velocity, fill in a missing value for east and west
    key = 'wind_north'
    for index in range (0,len(data[key])):
        if data['wind_speed'][index] == generalMissingValue:
            data['wind_north'][index] = generalMissingValue
            data['wind_east'][index] = generalMissingValue
        
        data['wind_north'][index]=float(data['wind_north'][index])
        data['wind_east'][index]=float(data['wind_east'][index])

    return data