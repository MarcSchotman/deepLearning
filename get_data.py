# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:57:16 2018

SUMMARY: SAVES ALL DATA LISTED IN KEYS FOR EACH WEATHER STATION IN THE LIST FOR EACH EYAR IN THE LIST PER YEAR USING PIKCLE

@author: m_a_s
"""
def get_data(YEARS,USAF_ID, WBAN_ID, keys,destinationPath):
    import ftplib
    import io
    import gzip
    import ish_parser# from: https://github.com/haydenth/ish_parser
    import pickle
    import os.path
    ftp_host = "ftp.ncdc.noaa.gov"
    parser = ish_parser.ish_parser()
    
    #concatenates the two ID's with '-' in between
    STATION_ID_LIST=["{}-{:2}".format(a_, b_) for a_, b_ in zip(USAF_ID, WBAN_ID)]
    
    #calculate total amount of years to keep track of progress
    total_years=0
    for years in YEARS:
        total_years+=1
        
    with ftplib.FTP(host=ftp_host) as ftpconn:
        ftpconn.login()
        counting=0
        for year in YEARS:
            percentage_done = counting/(total_years*100)
            counting+=1
            print("Downloading and processing files for year ", year,round(percentage_done,1),"% of total completed....")
            
            counting_inter =0
            #initilize dict for each year        
            data_year={}
            for station_id in STATION_ID_LIST:
                ftp_file = "pub/data/noaa/{YEAR}/{ID}-{YEAR}.gz".format(ID=station_id, YEAR=year)
                
                #show file download and percentage of completention
                counting_inter+=1
                percentage_done = counting_inter/len(STATION_ID_LIST)*100
                if int(len(STATION_ID_LIST)/10) ==0:
                    dummy_number = 1
                else:
                    dummy_number =  int(len(STATION_ID_LIST)/10)
                
                if counting_inter%dummy_number ==0:
                    print("Year ", year, " ", round(percentage_done,1),"% completed....")
        
                
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
            
            #time to save the dict
            file_name = str(year)
            full_path_name = os.path.join(destinationPath,file_name)
            
            if not os.path.exists(destinationPath):
                    os.makedirs(destinationPath)
                    
            #uses pikcle for dumping dictionary
            with open(full_path_name + '.pickle', 'wb') as handle:
                pickle.dump(data_year, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Finished downloads and processing of all files.")



