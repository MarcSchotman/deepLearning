# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:50:52 2018

@author: m_a_s
"""
import pickle
import os.path
path_deep = os.getcwd()
pathname= os.path.join(path_deep,'Data','2015.pickle')
with open(pathname,'rb') as handle:
    data = pickle.load(handle)
print(data['010240-99999']['air_temperature'])