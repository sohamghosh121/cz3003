"""
    Weather API from NEA
"""

import requests
from xml.etree import ElementTree
from cms.models import Weather, Haze
from django.contrib.gis.geos import Point


class WeatherAPI:

    """
            WeatherAPI Class for weather.py
    """
    API_KEY = '781CF461BB6606AD62B1E1CAA87ECA614712A08DDD7A7DC7'

    NOWCAST_URL = 'http://www.nea.gov.sg/api/WebAPI/?dataset=2hr_nowcast&keyref=%s' % API_KEY
    PSI_URL = 'http://www.nea.gov.sg/api/WebAPI?dataset=psi_update&keyref=%s' % API_KEY
    PM2_5_URL = 'http://www.nea.gov.sg/api/WebAPI?dataset=pm2.5_update&keyref=%s' % API_KEY

    def pull_update(self):
        """
                Pulls Weather info from NEA:
                Includes
                    - Weather Info
                    - PSI Info
                    - PM2.5 Info
        """
        try:
            w = self.pull_weather_update()
            p = self.pull_PSI_update()
            return w and p
        except:
            return False

    def pull_weather_update(self):
        """
            Pulls Nowcast data
        """
        r = requests.get(self.NOWCAST_URL)
        if (r.status_code == 200):
            root = ElementTree.fromstring(r.content)
            for area in root.iter('area'):
                district_name = area.get('name')
                lon = float(area.get('lon'))
                lat = float(area.get('lat'))
                con = area.get('forecast')
                w, created = Weather.objects.get_or_create(
                    districtname=district_name, location=Point(lon, lat))
                w.condition = con
                w.save()
            return True
        else:
            print r.status_code
            return False

    def pull_PSI_update(self):
        """
            Pulls PSI Data
        """
        r = requests.get(self.PSI_URL)
        if (r.status_code == 200):
            root = ElementTree.fromstring(r.content)
            haze_object = {}
            pt = Point(0, 0)
            for region in root.iter('region'):
                for child in region:
                    if child.tag == 'id':
                        haze_object['districtname'] = child.text
                    elif child.tag == 'latitude':
                        pt.y = float(child.text)
                    elif child.tag == 'longitude':
                        pt.x = float(child.text)
                    elif child.tag == 'record':
                        for reading in child:
                            if reading.get('type') == 'NPSI':
                                haze_object['PSI'] = int(reading.get('value'))
                            elif reading.get('type') == 'NPSI_PM25':
                                haze_object['PM25'] = int(reading.get('value'))
                            elif reading.get('type') == 'NPSI_PM10':
                                haze_object['PM10'] = int(reading.get('value'))
                haze_object['location'] = pt
                w, created = Haze.objects.get_or_create(
                    districtname=haze_object['districtname'], defaults=haze_object)
            w.save()
            return True
        else:
            print r.status_code
            return False

    def get_nowcast_details(self, short_form):
        """
                returns long form of nowcast
        """
        return {
            'BR': ('Mist', 'haze.png'),
            'CL': ('Cloudy', 'darkcloud.png'),
            'DR': ('Drizzle', 'lightrain.png'),
            'FA': ('Fair (Day)', 'sunny.png'),
            'FG': ('Fog', 'haze.png'),
            'FN': ('Fair (Night)', 'clearnight.png'),
            'FW': ('Fair & Warm', 'hot.png'),
            'HG': ('Heavy Thundery Showers with Gusty Winds', 'thunderstorm.png'),
            'HR': ('Heavy Rain', 'rain.png'),
            'HS': ('Heavy Showers', 'shower.png'),
            'HT': ('Heavy Thundery Showers', 'thunderstorm.png'),
            'HZ': ('Hazy', 'haze.png'),
            'LH': ('Slightly Hazy', 'haze.png'),
            'LR': ('Light Rain', 'lightrain.png'),
            'LS': ('Light Showers', 'lightrain.png'),
            'OC': ('Overcast', 'darkcloud.png'),
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
        }[short_form]

    def return_geo_json(self):
        """
                returns GeoJson Data to be added into map
        """
        weather = Weather.objects.all()
        geojson = {'type': 'FeatureCollection', 'features': []}
        for w in weather:
            longform, icon = self.get_nowcast_details(w.condition)
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
