"""
    Weather API from NEA
"""

import requests
from xml.etree import ElementTree
from cms.models import Weather
from django.contrib.gis.geos import Point
from pullapi import PullAPI


class WeatherAPI(PullAPI):

    """
            WeatherAPI Class for weather.py
    """
    NOWCAST_URL = "http://www.nea.gov.sg/api/WebAPI/?dataset=2hr_nowcast&keyref=781CF461BB6606AD62B1E1CAA87ECA614712A08DDD7A7DC7"

    def pullUpdate(self):
        """
                pulls nowcast weather info from NEA
        """
        r = requests.get(self.NOWCAST_URL)
        if (r.status_code == 200):
            root = ElementTree.fromstring(r.content)
            print root
            for area in root.iter('area'):
                districtname = area.get('name')
                lon = float(area.get('lon'))
                lat = float(area.get('lat'))
                con = area.get('forecast')
                w, created = Weather.objects.get_or_create(
                    districtname=districtname, location=Point(lon, lat))
                w.condition = con
                w.save()
            return True
        else:
            print r.status_code
            return False

    def getNowcastDetails(self, shortForm):
        """
                returns long form of nowcast
        """
        return {
            'BR': ('Mist', 'haze.png'),
            'CL': ('Cloudy', 'cloudy.png'),
            'DR': ('Drizzle', 'lightrain.png'),
            'FA': ('Fair (Day)', 'sunny.png'),
            'FG': ('Fog', 'haze.png'),
            'FN': ('Fair (Night)', 'clearnight'),
            'FW': ('Fair & Warm', 'hot.png'),
            'HG': ('Heavy Thundery Showers with Gusty Winds', 'thunderstorm.png'),
            'HR': ('Heavy Rain', 'rain.png'),
            'HS': ('Heavy Showers', 'shower.png'),
            'HT': ('Heavy Thundery Showers', 'thunderstorm.png'),
            'HZ': ('Hazy', 'haze.png'),
            'LH': ('Slightly Hazy', 'haze.png'),
            'LR': ('Light Rain', 'lightrain.png'),
            'LS': ('Light Showers', 'lightrain.png'),
            'OC': ('Overcast', 'cloud.png'),
            'PC': ('Partly Cloudy (Day)', 'partialsun.png'),
            'PN': ('Partly Cloudy (Night)', 'partialnight.png'),
            'PS': ('Passing Showers', 'shower.png'),
            'RA': ('Moderate Rain', 'rain.png'),
            'SH': ('Showers', 'shower.png'),
            'SK': ('Strong Winds, Showers', 'shower.png'),
            'SN': ('Snow', 'snow.png'),
            'SR': ('Strong Winds, Rain', 'rain.png'),
            'SS': ('Snow Showers', 'snow.png'),
            'SU': ('Sunny', 'sunny.png'),
            'SW': ('Strong Winds', 'superwindy.png'),
            'TL': ('Thundery Showers', 'thunderstorm.png'),
            'WC': ('Windy, Cloudy', 'windy.png'),
            'WD': ('Windy', 'windy.png'),
            'WF': ('Windy, Fair', 'windy.png'),
            'WR': ('Windy, Rain', 'rain.png'),
            'WS': ('Windy, Showers' 'shower.png')
        }[shortForm]

    def returnGeoJson(self):
        """
                returns GeoJson Data to be added into map
        """
        weather = Weather.objects.all()
        geojson = {'type': 'FeatureCollection', 'features': []}
        for w in weather:
            longform, icon = self.getNowcastDetails(w.condition)
            geojson['features'].append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [w.location.x, w.location.y]
                },
                'properties': {
                    'type': 'weather',
                    'name': w.districtname,
                    'condition_short': w.condition,
                    'condition_long': longform,
                    'icon': icon
                }
            })
        return geojson
