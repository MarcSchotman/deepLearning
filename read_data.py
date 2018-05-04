import ftplib
import re # for stripping name (#curcentStationName = curcentStationName.strip('-2017.gz'))

# loop over these years
yearStart = 2012
yearEnd = 2017
years = list(range(yearStart, yearEnd + 1))

# init
station = {}
station = station.fromkeys(years)
stationNames = {}

#Open ftp connection
#host name
ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()

# set path
ftp.cwd('pub/data/noaa/isd-lite/')
parent_dir = ftp.pwd()

for year in years:
    station[year] = [] # init dict as list
    
    print('Extracting year data from ' + str(year) + '.')
    ftp.cwd(str(year)) # go to year dict
    
    
    #List the files in the current directory
    stationFolder = []
    ftp.dir(stationFolder.append)         # list directory contents  
    
    
    for ii in stationFolder:
         
        # split the current line at spaces, and get last entry (where station ID is located)
        curcentStationID = ii.split(' ')[-1]
        
        # remove year.gz from station ID, and store station ID in dict
        curcentStationID = re.sub('-' + str(year) +'.gz', '', curcentStationID)
        station[year].append(curcentStationID)

    # Go to parent dictionary
    ftp.cwd('..')
    
# example
print(station[year][1])

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
