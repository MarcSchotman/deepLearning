# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:25:22 2018

@author: Taeke
"""

import numpy as np

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

isd_history_file = open('isd-history.txt', "r")
isd_history = isd_history_file.read()
isd_history = isd_history.split("\n") #

# clear text lines
del(isd_history[0:22])

print(isd_history[0])

data = []

for line in isd_history:
    lineNumber = []
    #lineSplit = line.split()
    lineSplit = line.split()
    
    for item in lineSplit:
        if string_is_number(item):
            lineNumber.append(item)
    

    data.append(lineNumber)
        
        
        
