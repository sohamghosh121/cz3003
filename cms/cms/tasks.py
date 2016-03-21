from __future__ import absolute_import
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import group
from datetime import timedelta
from cms.pullapis.dengue import DengueAPI
from cms.pullapis.weather import WeatherAPI
from cms.dispatchers.pmodispatcher import PMODispatcher
from cms.crisiscalculation.calculation import CrisisCalculator


logger = get_task_logger(__name__)


@task(name="pmo-emailer", bind=True)
def email_pmo(self):
    """
        Background task to send PMO email every half an hour
    """
    PMODispatcher().dispatch()
    return 'Success'


@task(name="do-pull-apis", bind=True)
def pull_apis(self):
    """
        Background task to periodically pull APIs for weather and dengue
    """
    apis = [WeatherAPI(), DengueAPI()]
    for api in apis:
        api.pull_update()
    return 'Success'


@task(name="check-for-crisis", bind=True)
def check_crisis(self):
    """
        Background task to periodically pull APIs for weather and dengue
    """
    CrisisCalculator().check_crisis()

@task(name="save-map-screenshots", bind=True)
def pull_apis(self):
    """
        Background task to periodically save screenshots
    """
    return 'Success'
