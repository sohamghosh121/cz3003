from __future__ import absolute_import
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import group
from datetime import timedelta


logger = get_task_logger(__name__)


@task(name="pmo_emailer", bind=True)
def email_pmo(self):
    return 'Success'


@task(name="do_pull_apis", bind=True)
