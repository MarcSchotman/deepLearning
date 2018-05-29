# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:01:24 2018

@author: m_a_s
"""

def make_missingValueDict():
    allFilterableKeys = ['air_temperature','sea_level_pressure','humidity','dew-point','wind_speed','wind_direction','wind_observation_direction_type']
    missingValueList ={}
    missingValueList = dict.fromkeys(allFilterableKeys)
    missingValueList['air_temperature'] = 999.9
    missingValueList['sea_level_pressure'] = 9999.9 
    missingValueList['humidity'] = 'MISSING'
    missingValueList['wind_speed'] =  999.9
    missingValueList['wind_direction'] =  999.9
    missingValueList['dew_point'] =  999.9 #<---this is random... NO VALUES IN DEWPOINT......
    missingValueList['wind_observation'] = '999'
    missingValueList['wind_observation_direction_type'] =  ''
    return missingValueList