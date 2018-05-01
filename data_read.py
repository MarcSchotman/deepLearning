import ftplib

yearFolder = [2017, 2016]
station = {}
station.fromkeys(yearFolder)


#Open ftp connection
# host name
ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()

# set path
ftp.cwd('pub/data/noaa/isd-lite/')

stationNames = {}

for i in yearFolder:
    print(i)
    ftp.cwd(str(i))
    
    
    #List the files in the current directory
    stationFolder = []
    ftp.dir(stationFolder.append)         # list directory contents  
    
    for ii in stationFolder:
        staion = ii.split(' ')[-1]


print(stationFolder[1])

   

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
