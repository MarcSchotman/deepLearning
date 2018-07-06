# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:43:32 2018

@author: m_a_s
"""
def match_dates(dateList, data_year, currentKeys, ID, maxDiff, missingValueList):
    #checks dates and fills in missing value if date difference is larger then  maxDiff
    
    index = 1 #NEEDS TO BE 1
    datesStation = data_year[ID]['datetime']
    outList = {}
    outList = dict.fromkeys(currentKeys)
    for key in currentKeys:
        outList[key] = []    
    for date in dateList:
        match = False
        last_delta = abs(date - datesStation[index-1])
        
        while match==False:
            delta = abs(date - datesStation[index])
            if delta > last_delta:
                match =True
                #makes sure that when at the last index it stays there i.e. not index+=1
            elif (index) == len(datesStation)-1:
                match =True
            else:
                #only continue if there was no match
                index +=1    
                last_delta = delta
        
        if last_delta > maxDiff:
            missing = True
        else:
            missing = False
            
        for key in currentKeys:
            if key == 'datetime':
                outList[key] = dateList
            elif missing and key !='latitude' and key !='longitude' and key != 'elevation' :
                outList[key].append(missingValueList[key])
            else:                    
                outList[key].append(data_year[ID][key][index])
    return outList
    