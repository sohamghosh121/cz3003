from django.db import models
from django.contrib.gis.db import models as gismodels


class Weather(gismodels.Model):
	districtname = models.CharField(max_length=128, primary_key=True)
	location = gismodels.PointField()
	condition = models.CharField(max_length=2, blank=True)

class Dengue(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    locality = models.CharField(max_length=254, blank=True, null=True)
    case_size = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    hyperlink = models.CharField(max_length=254, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_dengue'
