# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 17:40
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(default=b'', max_length=256)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(default=b'', max_length=256)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TerroristEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isactive', models.BooleanField(default=True)),
                ('description', models.TextField(default=b'')),
                ('numCasualties', models.IntegerField(default=0)),
                ('num_injured', models.IntegerField(default=0)),
                ('date_recorded', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326)),
                ('contact_number', models.CharField(blank=True, max_length=8)),
                ('assistance_required', models.CharField(choices=[(b'AMB', b'Ambulance'), (b'RES', b'Rescue'), (b'EVA', b'Evacuation')], max_length=3)),
                ('numHostiles', models.IntegerField(default=0)),
                ('attackType', models.CharField(choices=[(b'BMB', b'Bomb'), (b'BCH', b'Biochemical'), (b'HST', b'Hostage')], max_length=3)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Operator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrafficEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isactive', models.BooleanField(default=True)),
                ('description', models.TextField(default=b'')),
                ('numCasualties', models.IntegerField(default=0)),
                ('num_injured', models.IntegerField(default=0)),
                ('date_recorded', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326)),
                ('contact_number', models.CharField(blank=True, max_length=8)),
                ('assistance_required', models.CharField(choices=[(b'AMB', b'Ambulance'), (b'RES', b'Rescue'), (b'EVA', b'Evacuation')], max_length=3)),
                ('numVehicles', models.IntegerField(default=0)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Operator')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
