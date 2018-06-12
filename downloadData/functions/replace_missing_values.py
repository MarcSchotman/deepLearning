# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 20:11:33 2018

@author: m_a_s
"""

def replace_missing_values(station,keys,generalMissingValue,missingValueList):
    for key in keys:
        for index in range (0,len(station[key])):
            if station[key][index] == missingValueList[key]:
                station[key][index] = generalMissingValue
            
            station[key][index]=float(station[key][index])
    return station