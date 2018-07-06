# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:00:16 2018

@author: m_a_s
"""


def desired_date_list(year,measurementsADay):
    import datetime    
    import pytz
    from get_number_of_hours_year import get_number_of_hours_year
    #create range of dates
    base = datetime.datetime(year, 1, 1, 0, 0, tzinfo = pytz.UTC)
    numHours = get_number_of_hours_year(year)
    
    dateList = [base + datetime.timedelta(hours=x) for x in range(0, numHours, int(24/measurementsADay))]
    return dateList