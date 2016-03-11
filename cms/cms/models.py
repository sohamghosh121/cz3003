from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User


class Operator(User):
    name = models.CharField(max_length=256, default='')


class Admin(User):
    name = models.CharField(max_length=256, default='')


class Event(models.Model):
	AMBULANCE = 'AMB'
    RESCUE = 'RES'
    EVACUATION = 'EVA'
    TYPE_CHOICES = (
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
    contact_number = models.CharField(max_length=8)
    assistance_required = models.CharField(max_length=3, choices=ASSISTANCE_CHOICES)


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
