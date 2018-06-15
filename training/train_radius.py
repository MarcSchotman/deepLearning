# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:30:19 2018

@author: Taeke
"""
# data/RADIUS500KM/

from train import train

radii = [100]
f = ['air_temperature']

for r in radii:
    train(radius = r, features_train = f)