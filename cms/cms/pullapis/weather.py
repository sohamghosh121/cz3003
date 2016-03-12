"""
	Weather API from NEA
"""

import requests
from xml.etree import ElementTree
from cms.models import Weather
from django.contrib.gis.geos import Point
from django.test import TestCase

class WeatherAPI:
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
				w, created = Weather.objects.get_or_create(districtname=districtname, location=Point(lon, lat))
				w.condition = con
				w.save()
			return True
		else:
			print r.status_code
			return False

	def getLongNowcast(self, shortForm):
		"""
			returns long form of nowcast
		"""
		return {
			'BR': 'Mist',
			'CL': 'Cloudy',
			'DR': 'Drizzle',
			'FA': 'Fair (Day)',
			'FG': 'Fog',
			'FN': 'Fair (Night)',
			'FW': 'Fair & Warm',
			'HG': 'Heavy Thundery Showers with Gusty Winds',
			'HR': 'Heavy Rain',
			'HS': 'Heavy Showers',
			'HT': 'Heavy Thundery Showers',
			'HZ': 'Hazy',
			'LH': 'Slightly Hazy',
			'LR': 'Light Rain',
			'LS': 'Light Showers',
			'OC': 'Overcast',
			'PC': 'Partly Cloudy (Day)',
			'PN': 'Partly Cloudy (Night)',
			'PS': 'Passing Showers',
			'RA': 'Moderate Rain',
			'SH': 'Showers',
			'SK': 'Strong Winds, Showers',
			'SN': 'Snow',
			'SR': 'Strong Winds, Rain',
			'SS': 'Snow Showers',
			'SU': 'Sunny',
			'SW': 'Strong Winds',
			'TL': 'Thundery Showers',
			'WC': 'Windy, Cloudy',
			'WD': 'Windy',
			'WF': 'Windy, Fair',
			'WR': 'Windy, Rain',
			'WS': 'Windy, Showers'
		} [shortForm]

	def test(self):
		print self.getLongNowcast( 'PN')
	
	def returnGeoJson (self):
		"""
			returns GeoJson Data to be added into map
		"""
		weather = Weather.objects.all
		geojson = {'type': 'FeatureCollection', 'features': []}
		for w in weather :
			geojson.features.append({
				'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [w.location.x, w.location.y]
                },
                'properties': {
                    'name': p.districtname,
                    'condition_short': p.condition,

                }
			})


