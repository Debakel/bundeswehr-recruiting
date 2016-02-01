import googlemaps
import csv
from geojson import Feature, Point, FeatureCollection

from os import listdir

gmaps = googlemaps.Client(key='AIzaSyArKlZODWO33qKEo3fWsKeaxBD-MjoL3Do')
dir = 'data/'
data = []

for filename in listdir(dir):
    with open(dir + filename) as csvfile:
        print( 'Lese ' + filename)
        reader = csv.reader(csvfile, delimiter=',', )
        for row in reader:
            description = row[0]
            zeitraum = row[1]
            von_bis = row[2]
            dauer = row[3]
            plz = row[4]
            ort = row[5]

            r = gmaps.geocode(ort)
            lng = r[0]['geometry']['location']['lng']
            lat = r[0]['geometry']['location']['lat']

            point = Point((lng, lat))
            feature = Feature(geometry=point, properties = {
                'desc': description,
                'zeitraum': zeitraum,
                'ort': ort,
            })
            data.append(feature)

feature_collection = FeatureCollection(data)
print(feature_collection)