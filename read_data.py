import ftplib
import re # for stripping name (#curcentStationName = curcentStationName.strip('-2017.gz'))

# loop over these years
yearStart = 2012
yearEnd = 2013
years = list(range(yearStart, yearEnd + 1))
keys = ['USAF', 'WBAN'] # for station list

# init
stationYear = {}
stationYear = stationYear.fromkeys(years)
# stationID = {}

#Open ftp connection
#host name
ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()

# set path
ftp.cwd('pub/data/noaa/isd-lite/')
parent_dir = ftp.pwd()

for year in years:
    stationYear[year] = [] # init dict as list
    
    # reset dict
#    stationID = stationID.fromkeys(keys)
#    for key in keys:
#                stationID[key] = []
    
    
    print('Extracting year data from ' + str(year) + '.')
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
        
        # map to int
        curcentStationID = list(map(int, curcentStationID))
         
        stationYear[year].append(curcentStationID)
        
        # add station ID to dict
        # stationID[keys[0]].append(curcentStationID[0])
        # stationID[keys[1]].append(curcentStationID[1])
        
    # add station to corresponding year
    # stationYear[year] = stationID
    # Go to parent dictionary
    ftp.cwd('..')
    
# example
print(stationYear[year])

# Check which station was active in each year
activeEachYear = stationYear[2012]

for year in years:
    for stationID in stationYear[year]:
        
        if contains(activeEachYear, stationID)

stationYear2012 = stationYear[2012]
stat
result = cmp(stationYear[2012], stationYear[2012])


shared_items = set(stationYear2012.items()) & set(stationYear2012.items())
print(shared_items)

ftp.quit()

# cmp(dict1, dict2)
# =============================================================================
# #Get the readme file
# ftp.cwd("/pub")
# gFile = open("readme.txt", "wb")
# ftp.retrbinary('RETR Readme', gFile.write)
# gFile.close()

# 
# #Print the readme file contents
# print "\nReadme File Output:"
# gFile = open("readme.txt", "r")
# buff = gFile.read()
# print buff
# gFile.close()
# =============================================================================
