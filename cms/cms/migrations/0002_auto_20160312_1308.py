# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 13:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtransactionlog',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Admin'),
        ),
        migrations.AddField(
            model_name='eventtransactionlog',
            name='date_transaction',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 3, 12, 13, 8, 54, 836503, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventtransactionlog',
            name='desc',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
