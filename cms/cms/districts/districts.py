import os
import json
from django.core.serializers import serialize
from cms.models import Singapore, Districts, CrisisTransactionLog
from django.contrib.gis.geos import Point
from ..dispatchers.socialmediadispatcher import SocialMediaDispatcher


class DistrictManager():

    """
            handles district shp files
    """
    # DISTRICT_SHP_FILENAME = "cms/districts/SGP_adm1.shp"
    # EAST_CENTER = Point(1.3573764,103.9397103)
    # NORTH_EAST_CENTER = Point(1.382384, 103.876254)
    # NORTH_CENTER = Point (1.4215094,103.7952563)
    # WEST_CENTER = Point(1.3668943,103.7071299)
    # CENTRAL_CENTER = Point(1.2903924,103.8242863)
    # def importDistricts(self):
    #   """ imports districts of Singapore into database"""
    #   command_to_run = "shp2pgsql -d -W LATIN1 %s cms_singapore | psql -d cms" % self.DISTRICT_SHP_FILENAME
    #   os.system(command_to_run)
    #   for x in Singapore.objects.all():
    #       d, created = Districts.objects.get_or_create(
 #                    district=x.name_1)
    #       if (d.district == "East"):
    #           d.center = self.EAST_CENTER
    #       if (d.district == "North-East"):
    #           d.center = self.NORTH_EAST_CENTER
    #       if (d.district == "West"):
    #           d.center = self.WEST_CENTER
    #       if (d.district == "North"):
    #           d.center = self.NORTH_CENTER
    #       if (d.district == "Central"):
    #           d.center = self.CENTRAL_CENTER
    #       d.save()

    def returnGeoJson(self):
        """ 
                returns GeoJsonData for district boundaries
        """
        # self.importDistricts()
        singapore = Singapore.objects.all()
        singaporeJson = json.loads(serialize('geojson', singapore))
        for x in singaporeJson['features']:
            x['properties']['type'] = 'district'
            x['properties']['crisis'] = Districts.objects.get(
                district=x['properties']['name_1']).crisis
            x['properties']['center'] = [float(Districts.objects.get(district=x['properties']['name_1']).center.x), float(
                Districts.objects.get(district=x['properties']['name_1']).center.y)]
        return singaporeJson


class CrisisManager ():

    """ 
            Handle changing of crisis levels and crisis log
    """

    def setCrisisLevel(self, district_to_set, crisis_to_set, admin):
        """
                Sets crisis level of a specified district and add to log
        """
        d = Districts.objects.get(district=district_to_set)
        if (d is not None):
            d.crisis = crisis_to_set
            d.save()
        log = CrisisTransactionLog(
            district=district_to_set, new_crisis=crisis_to_set)
        log.save()
        SocialMediaDispatcher(log).dispatch()
