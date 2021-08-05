#Justin Sullivan ACO240
import csv

#Storm object consists of an id, origin, storm number, year, name, and a list of observation observed for each storm object.
class Storm:
    def __init__(self, id, origin, storm_num, year, name):
        self._id = id
        self._origin = origin
        self._storm_num = storm_num
        self._year = year
        self._name = name
        self._observation = []
        
    #Represents all variables for the Storm class
    def __repr__(self):
        return '('+self._id+', '+self._origin+', '+str(self._storm_num)+', '+str(self._year)+', '+self._name+', '+str(len(self._observation))+')'

    #adds observations to the list observations
    def add_observation(self, obs):
        self._observation.append(obs)

    #returns the id of the storm
    def get_id(self):
        return self._id

    #returns the origin of the storm
    def get_origin(self):
        return self._origin

    #returns the storm number
    def get_storm_num(self):
        return self._storm_num

    #returns the year of the storm
    def get_year(self):
        return self._year

    #returns the name of the storm
    def get_name(self):
        return self._name

    #returns a list of observations made
    def get_observation(self):
        return self._observation

#observation class consisting of a storm, date, time, status, latitude, longitude, max wind speed, and min pressure, creates an object of observations that are add to the storm class observation list.
class Observation:
    def __init__(self, storm, date, time, status, latitude, longitude, max_wind, min_pressure):
        self._storm = storm
        self._date = date
        self._time = time
        self._status = status
        self._latitude = latitude
        self._longitude = longitude
        self._max_wind = max_wind
        self._min_pressure = min_pressure

    #Represents all variables for observation class
    def __repr__(self):
        return '('+self._storm.get_name()+', '+str(self._date)+', '+str(self._time)+', '+str(self._status)+', '+self._latitude+', '+self._longitude+', '+str(self._max_wind)+', '+str(self._min_pressure)+')'

    #returns the storms
    def get_storm(self):
        return self._storm

    #returns the date that the storm occured
    def get_date(self):
        return self._date

    #returns the time of the storm
    def get_time(self):
        return self._time

    #returns the status of the storm
    def get_status(self):
        return self._status

    #returns the latitude of the storm
    def get_latitude(self):
        return self._latitude

    #returns the longitude of the storm
    def get_longitude(self):
        return self._longitude

    #returns the max wind of the storm
    def get_max_wind(self):
        return self._max_wind

    #returns the min pressure of the storm
    def get_min_pressure(self):
        return self._min_pressure

#Tester code
origin_year_dict = {}
oy_tuple = ()
with open('storms_three_years.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: #reads each row of the csv file.
        ID = row['ID']
        oy_tuple = (ID[0:2], int(ID[4:]))
        if  oy_tuple not in origin_year_dict: #if key is not in the dictionary, a key value  pair is established
            storm_obj = Storm(ID, ID[0:2], int(ID[2:4]), int(ID[4:]), row['Name'])
            obv = Observation(storm_obj, int(row['Date']), int(row['Time']), row['Status'], row['Latitude'], row['Longitude'], int(row['Maximum Wind']), int(row['Minimum Pressure']))
            storm_obj.add_observation(obv)
            origin_year_dict[oy_tuple] = [storm_obj]
        else: #if the key is already inside the dictionary
            if ID in [s.get_id() for s in origin_year_dict[oy_tuple]]: #checks if the ID is in the dictionary, if not, it is add with a observation.
                st = [s for s in origin_year_dict[oy_tuple] if s.get_id() == ID][0]
                obv = Observation(st, int(row['Date']), int(row['Time']), row['Status'], row['Latitude'], row['Longitude'], int(row['Maximum Wind']), int(row['Minimum Pressure']))
                st.add_observation(obv)
            else: #if the ID is in the dictionary, it will add an observation object to the storm object.
                storm_obj = Storm(ID, ID[0:2], int(ID[2:4]), int(ID[4:]), row['Name'])
                obv = Observation(storm_obj, int(row['Date']), int(row['Time']), row['Status'], row['Latitude'], row['Longitude'], int(row['Maximum Wind']), int(row['Minimum Pressure']))
                storm_obj.add_observation(obv)
                origin_year_dict[oy_tuple].append(storm_obj)

status_dict = {}
status_code = ['HU', 'TS', 'SS', 'TD', 'SD', 'EX', 'LO', 'WV', 'DB']
for status in status_code: #each status in status_code will look for storms that are associated with that status
    val = [v for v in origin_year_dict.values()]
    obs = [o.get_observation() for v in val for o in v]
    st_stat = [s for x in obs for s in x if s.get_status().strip() == status]
    storm_name = [s.get_storm() for s in st_stat]
    status_dict[status] = (storm_name, [o for o in st_stat if o.get_storm() == storm_name])
    
print('OUTPUT 1')
for k,v in sorted(origin_year_dict.items(), key=lambda y:(y[0][1], y[0][0]), reverse=True): #for each key and value in the dictionary, it will sort by pos 0 and 1 in the dictionary.
    print(k[1],k[0], len(v), sorted([y.get_name().strip() for y in (v)]))

print('OUTPUT 2')
output_years = set([year for (origin,year) in origin_year_dict.keys()])
for year in sorted(output_years, reverse=True): #for each year in the set output_year, it will check to see if the storm object has the same year and add it to a list.
    st_year = [s for x in origin_year_dict.values() for s in x if s.get_year() == year]
    print(year, len(st_year))
    max_min_tuple = [(s.get_name().strip(), max([mw.get_max_wind() for mw in s.get_observation()]), min([mp.get_min_pressure() for mp in s.get_observation()])) for s in st_year]
    for name, max_wind, min_pressure in sorted(max_min_tuple, key=lambda x: x[1], reverse=True): #takes a tuple and unpacks each value and prints, sorts the tuple by x=max_wind speed
        print(name, max_wind, min_pressure)

print('OUTPUT 3')