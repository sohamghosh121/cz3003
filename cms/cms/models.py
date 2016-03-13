from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User


class Weather(gismodels.Model):
    districtname = models.CharField(max_length=128, primary_key=True)
    location = gismodels.PointField()
    condition = models.CharField(max_length=2, blank=True)


class Haze(gismodels.Model):
    districtname = models.CharField(max_length=128, primary_key=True)
    location = gismodels.PointField()
    PSI = models.IntegerField(default=0)
    PM25 = models.IntegerField(default=0)
    PM10 = models.IntegerField(default=0)


class Dengue(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    locality = models.CharField(max_length=254, blank=True, null=True)
    case_size = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    hyperlink = models.CharField(max_length=254, blank=True, null=True)
    shape_leng = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = gismodels.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_dengue'


class Operator(User):
    name = models.CharField(max_length=256, default='')


class Admin(User):
    name = models.CharField(max_length=256, default='')


class Reporter(models.Model):
    name = models.CharField(max_length=128, default='')
    identification = models.CharField(max_length=10, primary_key=True)
    contact_number = models.CharField(max_length=8, blank=True)


class Event(models.Model):
    AMBULANCE = 'AMB'
    RESCUE = 'RES'
    EVACUATION = 'EVA'
    ASSISTANCE_CHOICES = (
        (AMBULANCE, 'Ambulance'),
        (RESCUE, 'Rescue'),
        (EVACUATION, 'Evacuation')
    )

    operator = models.ManyToManyField(Operator)
    first_responder = models.ForeignKey(
        Reporter, related_name='first_responder')
    reporters = models.ManyToManyField(
        Reporter, blank=True, related_name='other_responders')
    isactive = models.BooleanField(default=True)
    description = models.TextField(default='')
    num_casualties = models.IntegerField(default=0)
    num_injured = models.IntegerField(default=0)
    date_recorded = models.DateTimeField(auto_now=True)
    location = gismodels.PointField(blank=True)
    assistance_required = models.CharField(
        max_length=3, choices=ASSISTANCE_CHOICES)


class TrafficEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_vehicles = models.IntegerField(default=0)


class TerroristEvent(models.Model):
    BOMB = 'BMB'
    BIOCHEMICAL = 'BCH'
    HOSTAGE = 'HST'
    TYPE_CHOICES = (
        (BOMB, 'Bomb'),
        (BIOCHEMICAL, 'Biochemical'),
        (HOSTAGE, 'Hostage')
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_hostiles = models.IntegerField(default=0)
    attack_type = models.CharField(max_length=3, choices=TYPE_CHOICES)


class EventTransactionLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=2, choices=(('ED', 'Edit'), ('CR', 'Create'), ('DL', 'Delete')))
    operator = models.ForeignKey(Operator, blank=True, null=True)
    reporter = models.ForeignKey(Reporter, blank=True, null=True)
    admin = models.ForeignKey(Admin, blank=True, null=True)
    desc = models.CharField(max_length=1024, blank=True)
    date_transaction = models.DateTimeField(auto_now=True)

class Singapore(models.Model):
    gid = models.AutoField(primary_key=True)
    id_0 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    iso = models.CharField(max_length=3, blank=True, null=True)
    name_0 = models.CharField(max_length=75, blank=True, null=True)
    id_1 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    name_1 = models.CharField(max_length=75, blank=True, null=True)
    hasc_1 = models.CharField(max_length=15, blank=True, null=True)
    ccn_1 = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    cca_1 = models.CharField(max_length=254, blank=True, null=True)
    type_1 = models.CharField(max_length=50, blank=True, null=True)
    engtype_1 = models.CharField(max_length=50, blank=True, null=True)
    nl_name_1 = models.CharField(max_length=50, blank=True, null=True)
    varname_1 = models.CharField(max_length=150, blank=True, null=True)
    geom = gismodels.GeometryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cms_singapore'

class Districts(models.Model):
    district = models.CharField(max_length=10, primary_key= True)
    crisis = models.PositiveSmallIntegerField(default = 0)
    center = gismodels.PointField(blank=True, null=True)

class CrisisTransactionLog(models.Model):
    new_crisis = models.PositiveSmallIntegerField()
    admin = models.ForeignKey(Admin, blank=True, null=True)
    district = models.CharField(max_length=10)
    date_recorded = models.DateTimeField(auto_now=True)

