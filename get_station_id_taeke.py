# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:25:22 2018

@author: Taeke
"""

import math
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

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

def select_id_radius(dataIn, long, lat, r):
    
    rEarth = 6371
    theta = (r/rEarth) * (180/ math.pi)
    print(theta)
    dataOut = []
    
    for line in dataIn:
        latCurrent = line[2]
        lonCurrent = line[3]
        dist = math.sqrt((lat - latCurrent)**2 + (lon - lonCurrent)**2)
        if dist < theta:
            dataOut.append(line)
            
    return dataOut

## start of script
isd_history_file = open('isd-history.txt', "r")
isd_history1 = isd_history_file.read()
isd_history = isd_history1.split("\n") #

# clear text lines
del(isd_history[0:22])

data = []
i=0
for line in isd_history:
    lineNumeric = []
    #lineSplit = line.split()
    lineSplit = line.split()
    
    for item in lineSplit:
        if string_is_number(item):
            lineNumeric.append(item)
    
    if check_numbers(lineNumeric):  
        data.append(convert_number(lineNumeric))

lon = 4.3571
lat = 52.0116
r = 100 #radius in km
yearMin = 2015
yearMax = 2018
  
dataFiltered = select_id_radius(data, lon, lat, r)



#
lats = []
lons = []
for line in dataFiltered:
    lats.append(line[2])
    lons.append(line[3])

# draw map with markers for float locations
m = mpl_toolkits.basemap(projection='hammer',lon_0=180)
x, y = m(lons,lats)
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
m.scatter(x,y,3,marker='o',color='k')
plt.title('Locations of %s ARGO floats active between %s and %s' %\
        (len(lats)),fontsize=12)
plt.show()

    