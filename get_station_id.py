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
    
    
isd_history_file = open('isd-history.txt', "r")
isd_history1 = isd_history_file.read()
isd_history = isd_history1.split("\n") #

# clear text lines
del(isd_history[0:22])

data = []
i=0
for line in isd_history:
    lineNumber = []
    #lineSplit = line.split()
    lineSplit = line.split()
    
    for item in lineSplit:
        if string_is_number(item):
            lineNumber.append(item)
    
    if check_numbers(lineNumber):
        data.append(lineNumber)
        
  

