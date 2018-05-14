# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:50:52 2018

@author: m_a_s
"""
import pickle
import os.path

mapname= os.path.join('C:\\Users\\m_a_s\\Documents\\DUMMYDATA','RADIUS50KM')

with open(mapname+'\\2017.pickle','rb') as handle:
    data = pickle.load(handle)
with open(mapname + '\\STATION_ID.pickle','rb') as handle:
    station_id = pickle.load(handle)
    
STATION_ID_LIST=["{}-{:2}".format(a_, b_) for a_, b_ in zip(station_id[0], station_id[1])]
count =0
for time in data[STATION_ID_LIST[1]]['datetime']:
    print(time)
    count+=1
print(count)