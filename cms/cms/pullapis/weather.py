"""
	Weather API from NEA
"""

import requests
from xml.etree import ElementTree
from cms.models import Weather
from django.contrib.gis.geos import Point
from django.test import TestCase

class WeatherAPI:
	NOWCAST_URL = "http://www.nea.gov.sg/api/WebAPI/?dataset=2hr_nowcast&keyref=781CF461BB6606AD62B1E1CAA87ECA614712A08DDD7A7DC7"
	def pullUpdate(self): 
		"pulls nowcast weather info from NEA"
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

