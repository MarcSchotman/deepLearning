# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:25:22 2018

@author: Marc & Taeke
"""



def filter_stations(minStartDate, minEndDate, r_max, longitudeCenter, lattitudeCenter):
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    import ftplib
    import re # for stripping name (#curcentStationName = curcentStationName.strip('-2017.gz'))
     
    
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
       
    def plot_stations(stations):
        m = Basemap(projection='hammer',lon_0=0) #(projection = 'merc', llcrnrlat=30, urcrnrlat=90, llcrnrlon=-30, urcrnrlon=-35)
        #
        m.drawcoastlines()
        m.fillcontinents (color='lightgray', lake_color='lightblue')
        # m.drawparallels(np.arange(-90.,91.,30.))
        # m.drawmeridians(np.arange(-180.,181.,60.))
        m.drawmapboundary(fill_color='aqua')
        
        m.drawcounties()
        x, y = m(stations['LON'],stations['LAT'])
        #x, y = m(*zip(*[hawaii, austin, washington, chicago, losangeles]))
        m.plot(x,y, marker ='o', markersize=5, markerfacecolor='red', linewidth=0)
        #
        plt.title('Mercator Projection')
        plt.show()    
    
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
    
    def filter_station_date(stations,keys,minStartDate, minEndDate):
        beginDates = np.array(stations['BEGIN'])
        endDates = np.array(stations['END'])
        
        indexes = np.where((beginDates < minStartDate) & (endDates > minEndDate))
        
        #initilize stationsOut dict
        stationsOut ={}
        #takes only stations corresponding to indexes 
        for key in keys:
            stationsOut[key] = np.take(stations[key],indexes[0]) #INDEXES[0] NEEDED
        #np.where makes makes indexes an array in an array for some dark reason...
        return stationsOut
    
    def filter_station_radius(stations, keys, long, lat, r):
        
        rEarth = 6371
        theta = (r/rEarth) * (180/ math.pi)
        
        #initilize output dict
        stationsOut = {}
        for key in keys:
            stationsOut[key] = []
        
        #start filtering
        for index in range(0,np.size(stations['LAT'])):
            latCurrent = stations['LAT'][index]
            lonCurrent = stations['LON'][index]
            dist = math.sqrt((lat - latCurrent)**2 + (long - lonCurrent)**2)
            
            #if requirement is met this station is saved in stationsOut
            if dist < theta:
                for key in keys:
                    stationsOut[key].append(stations[key][index])
                
        return stationsOut
    
    def get_active_station_ids(years):
        
        # init
        stations = {}
        stations = stations.fromkeys(years)
        
        #Open ftp connection
        ftp = ftplib.FTP('ftp.ncdc.noaa.gov') #host name
        ftp.login()
        
        # set path
        ftp.cwd('pub/data/noaa/isd-lite/')
        parent_dir = ftp.pwd()
        
        for year in years:
            stations[year] = [] # init dict as list
                  
            print('Extracting year IDs from ' + str(year) + '.')
            ftp.cwd(str(year)) # go to year dict
              
            #List the files in the current directory
            stationFolder = []
            ftp.dir(stationFolder.append)         # list directory contents  
            
            for ii in stationFolder:
                 
                # split the current line at spaces, and get last entry (where station ID is located)
                curcentStationID = ii.split(' ')[-1]
                
                # remove year.gz from stationYears ID, and store stationYears ID in dict
                curcentStationID = re.sub('-' + str(year) +'.gz', '', curcentStationID)
                
                # split at -
                curcentStationID = curcentStationID.split('-')
                
                # append
                stations[year].append(curcentStationID)
                
            # Go to parent dictionary
            ftp.cwd('..')
            
        # close ftp connection
        ftp.quit()
        return stations
    
    def filter_station_activity(stationsIn,keys,minStartDate,minEndDate):
        
        #initilize output dict
        stationsOut = {}
        for key in keys:
            stationsOut[key] = []
        
        # get year list
        # easiest to only get first four numbers by converting to string, bit of a hack...
        yearStart = int(str(minStartDate)[:4])
        yearEnd = int(str(minEndDate)[:4])
        years = list(range(yearStart, yearEnd + 1))

        # get the IDs of stations which have been active in any of the selected years
        stations = get_active_station_ids(years)
        
        # Check which station was active in each year
        activeEachYear = stations[yearStart]
        delID = []
        
        # delete staions which are not active each year
        for year in years:
            print('Determine inactive station from Year: ' + str(year))
            delCount = 0
            # loop over active each year
            for ID in activeEachYear:
                # print(len(activeEachYear))
                if not(ID in stations[year]):
                    
                    delID.append(ID)
                    delCount = delCount + 1
                    
                    activeEachYear.remove(ID)
        
        # get Iindexes from stations we want to keep
        indexes = []
        delCount = 0
        
        for i in range(0, len(stationsIn[keys[0]])):
            
            currentStation = [stationsIn[keys[0]][i], stationsIn[keys[1]][i]]
            if (currentStation in activeEachYear):
                indexes.append(i)
            else:
                delCount = delCount + 1
               
        print(' Deleted ' + str(delCount) + ' inactive station(s)')
        
        for key in keys:
            stationsOut[key] = np.take(stationsIn[key],indexes)
            
        return stationsOut
    
    ## start of script
    isd_history_file = open('isd-history.txt', "r")
    isd_history1 = isd_history_file.read()
    isd_history = isd_history1.split("\n") #
    
    # clear text lines
    del(isd_history[0:22])
    
    #initilize dictionary
    stations ={}
    keys = ['USAF', 'WBAN', 'LAT', 'LON', 'ELEV', 'BEGIN', 'END']
    stations = stations.fromkeys(keys)
    #intilize dictionary as lists
    for key in keys:
                stations[key] = []
                
    for line in isd_history:
        lineNumeric = []
        #lineSplit = line.split()
        lineSplit = line.split()
        
        for item in lineSplit:
            if string_is_number(item):
                lineNumeric.append(item)
        
        if check_numbers(lineNumeric):  
            lineNumeric = convert_number(lineNumeric)
            
            for i in range(0,len(keys)):
                stations[keys[i]].append(lineNumeric[i])
    #longitude lattitude Delft, i.e. center of radius
    
    #        [ 0    1    2   3   4       5        6    ]  
    #stations = [USAF WBAN LAT LON ELEV BEGIN_DATE END_DATE]
    stations = filter_station_date(stations,keys,minStartDate,minEndDate)
    stations = filter_station_radius(stations,keys,longitudeCenter,lattitudeCenter,r_max)
    stations = filter_station_activity(stations,keys,minStartDate,minEndDate)
    
    plot_stations(stations)
    return stations

# test function
lattitudeCenter = 52.0116
longitudeCenter = 4.3571              
startDate = 20150101
endDate = 20170101
radius = 1000
stations = filter_stations(startDate, endDate, radius, longitudeCenter, lattitudeCenter)
# filter_stations(minStartDate, minEndDate, r_max, longitudeCenter, lattitudeCenter)