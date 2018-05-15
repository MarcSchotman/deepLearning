# -*- coding: utf-8 -*-
"""
Created on Tue May 15 10:49:01 2018

@author: m_a_s
"""

import datetime
import pytz
list2 = [datetime.datetime(2018, 3,4,0, 0,tzinfo=pytz.UTC)]
list1 = [datetime.datetime(2018, 3,4,0, 3,tzinfo=pytz.UTC), datetime.datetime(2018, 3,4,0,1,tzinfo=pytz.UTC), datetime.datetime(2018, 3,6,0, 0,tzinfo=pytz.UTC)]
import numpy as np
l1 = np.array(list1)
l2 = np.array(list2)

ind = abs(l1 - l2[:,None]) <= datetime.timedelta(0,0,0,0,60,0)

print(l1[ind.max(0)])
print(l2[ind.max(1)])
print(ind.max(1))
print(ind.max(0))
indexes_tuple = np.where(ind.max(0)==True)

indexes= [ index for index in indexes_tuple[0] ]

print(indexes)