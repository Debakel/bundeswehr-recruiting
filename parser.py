import googlemaps
import csv
from geojson import Feature, Point, FeatureCollection
import json
from os import listdir


def write_file(filename, text):
    with open(filename, 'w') as outfile:
        outfile.write(text)


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


gmaps = googlemaps.Client(key='AIzaSyBapNiIlZ8ZZ-j7rA9Z59S3BIzbZ2opob4')
geocoding = {}


def geocode(city):
    if city not in geocoding:
        result = gmaps.geocode(city + ', Germany')
        lng = result[0]['geometry']['location']['lng']
        lat = result[0]['geometry']['location']['lat']
        geocoding[city] = Point((lng, lat))

    return geocoding[city]


DESCRIPTION = 0
START = 1
END = 2
LENGTH = 3
PLZ = 4
CITY = 5

try:
    geocoding = json.loads(read_file('geocode.json'))
except:
    geocoding = {}
cities = {}

i = 0
data_dir = 'data/'
for filename in listdir(data_dir):
    with open(data_dir + filename) as csvfile:
        print('Lese ' + filename)
        reader = csv.reader(csvfile, delimiter=',', )
        row = reader.__next__()  # skip first row
        for row in reader:

            # Geocode city (only once per city)
            city = row[CITY]

            # Create event
            event = {
                'description': row[0],
                'start': row[1],
                'end': row[2],
                'length': row[3]
            }

            # Append event to city
            if city not in cities:
                cities[city] = Feature(geometry=geocode(city), properties=
                {
                    'title': city,
                    'plz': row[4],
                    'events': [event],
                    'description': '',
                    "icon": {
                        "className": "marker",
                        "html": "",
                        "iconSize": 'null'
                    }
                })
            else:
                cities[city].properties['events'].append(event)

            # Extend marker description
            cities[city].properties['description'] += '<b>{}</b><br>Zeitraum: {} - {}<br><br>' \
                .format(event['description'], event['start'], event['end'])

# Create feature list
features = []
for key, feature in cities.items():
    features.append(feature)
feature_collection = FeatureCollection(features)

# Write to file
write_file('features.geojson', json.dumps(feature_collection))
write_file('geocode.json', json.dumps(geocoding))
