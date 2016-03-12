from __future__ import absolute_import
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import group
from datetime import timedelta
from cms.pullapis.dengue import DengueAPI
from cms.pullapis.weather import WeatherAPI


logger = get_task_logger(__name__)


@task(name="pmo_emailer", bind=True)
def email_pmo(self):
    return 'Not implemented yet'


@task(name="do_pull_apis", bind=True)
def pull_apis(self):
    apis = [WeatherAPI(), DengueAPI()]
    for api in apis:
        api.pullUpdate()
    return 'Success'
