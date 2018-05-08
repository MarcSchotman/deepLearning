# -*- coding: utf-8 -*-
"""
Created on Fri May  4 10:16:42 2018

@author: m_a_s
"""

import ftplib

#Open ftp connection
# host name
ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
ftp.login()
ftp.cwd('/pub/data/noaa/') 

#isd-history contains a text file relating lattitude and attitude to station ID
gFile = open("isd-history.txt", "wb") #opens the file for reading
ftp.retrbinary('RETR isd-history.txt', gFile.write) #reads the file nad saves it as isd-histry
gFile.close()

ftp.quit()