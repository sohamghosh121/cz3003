from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User


class Operator(User):
    name = models.CharField(max_length=256, default='')


class Admin(User):
    name = models.CharField(max_length=256, default='')


class Event(models.Model):
    operator = models.ForeignKey(Operator)
    isactive = models.BooleanField(default=True)
    description = models.TextField()
    numCasualties = models.IntegerField(default=0)
    numInjured = models.IntegerField(default=0)
    dateRecorded = models.DateTimeField(auto_now=True)
    location = gismodels.PointField()


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
