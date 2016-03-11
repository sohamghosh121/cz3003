from django.db import models
from django.contrib.gis.db import models as gismodels


class Weather(gismodels.Model):
	districtname = models.CharField(max_length=128, primary_key=True)
	location = gismodels.PointField()
	condition = models.CharField(max_length=2, blank=True)
