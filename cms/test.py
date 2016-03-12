from django.test import TestCase
from cms.pullapis.weather import WeatherAPI

class WeatherAPITest(TestCase):
	def weatherTest(self):
		WeatherAPI().test()