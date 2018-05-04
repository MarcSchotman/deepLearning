# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:25:22 2018

@author: Taeke
"""

import numpy as np
import math

def string_is_number(s):
    if s[0] in ('-', '+'):
        return is_number(s[1:])
    return is_number(s)



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_numbers(s):
    #checking variables
    checking = True
    succes = False
    
    while checking:

        #if length of numbers is too small (i.e. cannot contain 2 ID numbers + 
        # 2 lattitude numbers + begin and end date)
        if len(s) < 6:
            checking = False 
        #check if third number starts with '+' or '-'
        elif s[2][0] != '+' and s[2][0] !='-':
            del(s[2])
        #check if fourth number starts with '+' or '-' 
        elif s[3][0] !='+' and s[3][0] !='-':
            del(s[3])
        #remove if eleveation not present
        elif s[4][0]!='+' and s[4][0] !='-':
            del(s[4])
        #if long enough and lattitudes + elevation is present data is OK
        else:
            succes =True
            checking = False
    
    return succes
      
def convert_number(s):
    line = []
    count = 0
    for item in s:
        
        if count == 0 or count == 1:
            newItem = item
        elif count == 2 or count == 3 or count == 4:
            if item[0] == '+':
                number = item[1:-1]
            number = item
            newItem = float(number)
        elif count == 5 or count == 6:
            newItem = int(item)
        
        line.append(newItem)
        count = count + 1
    return line

#def check_date(minStartDate, minEndDate, stations):
#    beginDates = np.array(stations['BEGIN'])
#    endDates = np.array(stations['END'])
#    
#    indexes = np.where(beginDates < minStartDate and endDates > minEndDate)
#    return indexes
    

## start of script
isd_history_file = open('isd-history.txt', "r")
isd_history1 = isd_history_file.read()
isd_history = isd_history1.split("\n") #

# clear text lines
del(isd_history[0:22])

#initilize dictionary
stations ={}
key = ['USAF', 'WBAN', 'LAT', 'LON', 'ELEV', 'BEGIN', 'END']
stations = stations.fromkeys(keys)
#intilize dictionary as lists
for i in range(0,7):
            stations[key[i]] = []
            
for line in isd_history:
    lineNumeric = []
    #lineSplit = line.split()
    lineSplit = line.split()
    
    for item in lineSplit:
        if string_is_number(item):
            lineNumeric.append(item)
    
    if check_numbers(lineNumeric):  
        lineNumeric = convert_number(lineNumeric)
        
        for i in range(0,7):
            stations[key[i]].append(lineNumeric[i])

lat = 52.0116
lon = 4.3571

minStartDate = int(20150000) #YearMonthDay
minEndDate = int(20180000)  #YearMonthDay

#        [ 0    1    2   3   4       5        6    ]  
#stations = [USAF WBAN LAT LON ELEV BEGIN_DATE END_DATE]
#indexes = check_date(minStartDate,minEndDate,stations)



    