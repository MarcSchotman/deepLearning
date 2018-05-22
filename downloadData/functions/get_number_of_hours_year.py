# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:41:44 2018

@author: m_a_s
"""

def get_number_of_hours_year(year): 
    if (year % 4) == 0 and (year % 100 != 0 or year % 400 == 0):
        days = 366
    else:
       days = 365
    return days * 24