from geopy.distance import vincenty


def find_closest_station(entries, position: (float, float)):
    """
    Finds the closest station to the given position in GPS coordinates.
    :param entries: Dictionary with station measurements
    :param position: GPS position (latitude, longitude)
    :return: id of the closest station, distance
    """
    min_dist = 1000000
    station_id_closest = list(entries.keys())[0]

    for station_id in entries.keys():

        try :
            dist = vincenty((entries[station_id]['latitude'][0], entries[station_id]['longitude'][0]), position).km
            if dist < min_dist:
                min_dist = dist
                station_id_closest = station_id
        except ValueError:
            print("ValueError: {}".format((entries[station_id]['latitude'][0], entries[station_id]['longitude'][0])))
    return station_id_closest, min_dist
