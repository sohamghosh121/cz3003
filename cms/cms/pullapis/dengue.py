"""
    Pulls dengue cluster information from data.gov.sg
"""

import requests
import zipfile
import os
import json
from cms.models import Dengue
from django.core.serializers import serialize
from pullapi import PullAPI


class DengueAPI(PullAPI):

    """
        DengueAPI Class for dengue.py
    """
    DENGUE_URL = "https://ref.data.gov.sg/common/Handler.ashx?ThemeName=DENGUE_CLUSTER&MetaDataID=227753&Format=shp"
    DENGUE_SHP_FILENAME = "DENGUE_CLUSTER.shp"
    DENGUE_ZIP_FILENAME = "DENGUE_CLUSTER.zip"
    DENGUE_EXTRACTED_FOLDER = "pullapis/dengue_extracted"

    def downloadFile(self, url, downloadFileName):
        r = requests.get(url, stream=True)
        if (r.status_code == 200):
            with open(downloadFileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            print r.status_code
            return False

    def unzip(self, zippedfile, extractLocation):
        try:
            zip = zipfile.ZipFile(zippedfile)
            zip.extractall(extractLocation)
            os.remove(zippedfile)
            return True
        except (zipfile.BadZipfile):
            print "error with zipfile"
            return False

    def updateDengueInfoInDatabase(self, fileDirectory):
        command_to_run = "shp2pgsql -s 3414 -d -W LATIN1 %s cms_dengue | psql -d cms" % fileDirectory
        os.system(command_to_run)

    def pullUpdate(self):
        try:
            if (self.downloadFile(self.DENGUE_URL, self.DENGUE_ZIP_FILENAME)):
                if (self.unzip(self.DENGUE_ZIP_FILENAME, self.DENGUE_EXTRACTED_FOLDER)):
                    fileDirectory = "%s/%s" % (
                        self.DENGUE_EXTRACTED_FOLDER, self.DENGUE_SHP_FILENAME)
                    self.updateDengueInfoInDatabase(fileDirectory)
                    return True
            return False
        except:
            return False

    def returnGeoJson(self):
        dengue = Dengue.objects.all()
        denguejson = json.loads(serialize('geojson', dengue))
        for x in denguejson['features']:
            x['properties']['type'] = 'dengue'
        return denguejson
