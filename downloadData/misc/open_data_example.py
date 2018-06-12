# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:50:52 2018

@author: m_a_s
"""
import pickle
import os.path
mapname = 'C:\\Users\\m_a_s\\Documents\\GitHub\\deepLearning\\data\\RADIUS100KM_PROCESSED'

with open(mapname+'\\2017.pickle','rb') as handle:
    data = pickle.load(handle)
with open(mapname + '\\STATION_ID.pickle','rb') as handle:
    STATION_ID_LIST = pickle.load(handle)
