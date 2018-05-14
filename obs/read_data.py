

# def get_continiously_active_station():
yearStart = 2012
yearEnd = 2014
years = list(range(yearStart, yearEnd + 1))

stations = get_active_station_ids(years)
# Check which station was active in each year
activeEachYearInit = stations[yearStart]

print('Initial length: ')
print(len(activeEachYearInit))
activeEachYear = activeEachYearInit
delCount = 0
delID = []

# delete staions which are not active each year
for year in years:
    print('==Start year==')
    print(year)
    
    # loop over active each year
    for ID in activeEachYear:
        # print(len(activeEachYear))
        if not(ID in stations[year]):
            
            delID.append(ID)
            delCount = delCount + 1
            
            activeEachYear.remove(ID)

print('final length')
print(len(activeEachYear))

print(delCount)
print(len(activeEachYear))

    # 1274