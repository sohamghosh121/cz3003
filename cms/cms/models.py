from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User


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
    geom = gismodels.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_dengue'


class Operator(User):
    name = models.CharField(max_length=256, default='')


class Admin(User):
    name = models.CharField(max_length=256, default='')


class Event(models.Model):
    AMBULANCE = 'AMB'
    RESCUE = 'RES'
    EVACUATION = 'EVA'
    ASSISTANCE_CHOICES = (
        (AMBULANCE, 'Ambulance'),
        (RESCUE, 'Rescue'),
        (EVACUATION, 'Evacuation')
    )

    operator = models.ForeignKey(Operator)
    isactive = models.BooleanField(default=True)
    description = models.TextField()
    numCasualties = models.IntegerField(default=0)
    num_injured = models.IntegerField(default=0)
    date_recorded = models.DateTimeField(auto_now=True)
    location = gismodels.PointField()
    contact_number = models.CharField(max_length=8, blank=True)
    assistance_required = models.CharField(
        max_length=3, choices=ASSISTANCE_CHOICES)


class TrafficEvent(Event):
    numVehicles = models.IntegerField(default=0)


class TerroristEvent(Event):
    BOMB = 'BMB'
    BIOCHEMICAL = 'BCH'
    HOSTAGE = 'HST'
    TYPE_CHOICES = (
        (BOMB, 'Bomb'),
        (BIOCHEMICAL, 'Biochemical'),
        (HOSTAGE, 'Hostage')
    )
    numHostiles = models.IntegerField(default=0)
    attackType = models.CharField(max_length=3, choices=TYPE_CHOICES)
