import ftplib
import re # for stripping name (#curcentStationName = curcentStationName.strip('-2017.gz'))


years = [2017]

# init
station = {}
station = station.fromkeys(years)
stationNames = {}

#Open ftp connection
# host name
ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()

# set path
ftp.cwd('pub/data/noaa/isd-lite/')



for year in years:
    station[year] = []
    
    print(year)
    ftp.cwd(str(year))
    
    
    #List the files in the current directory
    stationFolder = []
    ftp.dir(stationFolder.append)         # list directory contents  
    
    
    for ii in stationFolder:
        
        
        curcentStationName = ii.split(' ')[-1]
        
        curcentStationName = re.sub('-2017.gz', '', curcentStationName)
        station[year].append(curcentStationName)


print(station[year][1])

   

# cmp(dict1, dict2)
# =============================================================================
# #Get the readme file
# ftp.cwd("/pub")
# gFile = open("readme.txt", "wb")
# ftp.retrbinary('RETR Readme', gFile.write)
# gFile.close()
# ftp.quit()
# 
# #Print the readme file contents
# print "\nReadme File Output:"
# gFile = open("readme.txt", "r")
# buff = gFile.read()
# print buff
# gFile.close()
# =============================================================================
