# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:57:16 2018

SUMMARY: SAVES ALL DATA LISTED IN KEYS FOR EACH WEATHER STATION IN THE LIST FOR GIVEN YEAUSING PICKLE

@author: m_a_s
"""
def get_data(year,STATION_ID_LIST, keys,destinationPath):
    import ftplib
    import io
    import gzip
    import ish_parser# from: https://github.com/haydenth/ish_parser
    import os.path
    ftp_host = "ftp.ncdc.noaa.gov"
    parser = ish_parser.ish_parser()
    
    with ftplib.FTP(host=ftp_host, timeout = 600) as ftpconn:
        ftpconn.login()
        counting =0
        #initilize dict for each year        
        data_year={}
        print('Downloading year ', year)
        LastReportLength=0
        for station_id in STATION_ID_LIST:
            ftp_file = "pub/data/noaa/{YEAR}/{ID}-{YEAR}.gz".format(ID=station_id, YEAR=year)
            
            #show file download and percentage of completention
            counting+=1
            percentage_done = counting/len(STATION_ID_LIST)*100
            if int(len(STATION_ID_LIST)/10) ==0:
                dummy_number = 1
            else:
                dummy_number =  int(len(STATION_ID_LIST)/10)
            
            if counting%dummy_number ==0:
                print(round(percentage_done,1),"% completed....")
    
            
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
                
            #function from github which parses the nasty noaa data nicely for us.
            parser.loads(content)                
            reports = parser.get_reports()
            #selects the reports corresponding to the alst station
            reports = reports[LastReportLength:]
            LastReportLength += len(reports)
            
            #initilize nested dict for current station
            data_year[station_id] ={}
            #shows all possible keys (just so we remeber, dont delete please(!))
            possible_keys = dir(reports[0])
            
            #initilizes keys inside nested dictionary
            data_year[station_id] = data_year[station_id].fromkeys(keys)
            #initilize keys as lists so they can fit the year long features
            for i in keys:
                data_year[station_id][i] = []
            
            #append the features in the appropraite dictionary
            #slowest process in here: big nested loop.. loop1~6k, loop2=len(keys)
            
            for report in reports:
                for key in keys:
                    #get numerical data from the parsed matrix
                    value = getattr(report,key)
                    if key == 'humidity':
                        value_inserted = value.humidity
                    else:
                        try:
                            value_inserted = value._obs_value
                        except AttributeError:
                            
                            value_inserted = value
                    
                    data_year[station_id][key].append(value_inserted)
                    #getattr(report,i) makes it: report.i using the variable i.
                    #report['air_temperature'] for example gives the air temperature of this line
            reports = None
            content = None
        return data_year

#import os.path
##testing function
#lattitudeCenter = 52.0116
#longitudeCenter = 4.3571
#startYear = '2017'
#endYear = '2018'
#r_list = [40]
#STATION_ID = [['063300', '063430', '063440'], ['99999', '99999', '99999']]
#USAF_ID = STATION_ID[0]
#WBAN_ID = STATION_ID[1]
##concatenates the two ID's with '-' in between
#STATION_ID_LIST=["{}-{:2}".format(a_, b_) for a_, b_ in zip(USAF_ID, WBAN_ID)]
#    
#keys = ['datetime','air_temperature','humidity','elevation','dew-point','wind_speed','wind_direction','wind_observation_direction_type','longitude','latitude']
#minStartDate = int(startYear+'0000') #YearMonthDay
#minEndDate = int(endYear+'0000')  #YearMonthDay
#map_location = 'C:\\Users\\m_a_s\\Desktop\\data'
#mapName = 'RADIUS' + '40'+'KM'
#destinationPath = os.path.join(map_location,mapName)
#    
#    
#    
#YEARS = range(int(startYear), int(endYear))
#for year in YEARS:
#    [data_year, possible_keys] = get_data(year, STATION_ID_LIST,keys,destinationPath)
#    print(possible_keys)
