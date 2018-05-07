# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:57:16 2018

@author: m_a_s
"""

import ftplib
import io
import gzip
import ish_parser# from: https://github.com/haydenth/ish_parser
import pickle
import os.path
ftp_host = "ftp.ncdc.noaa.gov"
parser = ish_parser.ish_parser()

# identifies what data to get
USAF_ID = ['010240','010250','010260']
WBAN_ID = ['99999','99999','99999']
STATION_ID_LIST=["{}-{:2}".format(a_, b_) for a_, b_ in zip(USAF_ID, WBAN_ID)]
print(STATION_ID)

YEARS = range(2015, 2016)

with ftplib.FTP(host=ftp_host) as ftpconn:
    ftpconn.login()
    counting=0
    for year in YEARS:
        
        data_year={}
        for station_id in STATION_ID_LIST:
            ftp_file = "pub/data/noaa/{YEAR}/{ID}-{YEAR}.gz".format(ID=station_id, YEAR=year)
            
            percentage_done = counting/(len(YEARS)*len(STATION_ID_LIST))*100
            counting+=1
            print("Processing",ftp_file,"... ",percentage_done,"% completed")
    
            # read the whole file and save it to a BytesIO (stream)
            response = io.BytesIO()
            try:
                ftpconn.retrbinary('RETR '+ftp_file, response.write)
            except ftplib.error_perm as err:
                if str(err).startswith('550 '):
                    print('ERROR:', err)
                else:
                    raise
    
            # decompress and parse each line 
            response.seek(0) # jump back to the beginning of the stream
            with gzip.open(response, mode='rb') as gzstream:
                
                content =bytes.decode(gzstream.read())
                gzstream.close()
                
            
            parser.loads(content)                
            reports = parser.get_reports()  
            lenReport = len(reports)
            
            data_year[station_id] ={}
            possible_keys = dir(reports[0])
            keys = ['air_temperature','humidity','elevation','dew-point']#,'wind_speed','wind_direction','wind_observation_direction_type'
            data_year[station_id] = data_year[station_id].fromkeys(keys)
            #initilize dict
            for i in keys:
                data_year[station_id][i] = []
    
            for report in reports:
                for i in keys:                
                    data_year[station_id][i].append(getattr(report, i ))
                    
        path_deepLearning = os.getcwd()
        folder_name = 'Data'
        file_name = str(year)
        full_path_name = os.path.join(path_deepLearning,folder_name,file_name)
            
        with open(full_path_name + '.pickle', 'wb') as handle:
            pickle.dump(data_year, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
