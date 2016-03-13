# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Dengue',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('objectid', models.IntegerField(blank=True, null=True)),
                ('locality', models.CharField(
                    blank=True, max_length=254, null=True)),
                ('case_size', models.SmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(
                    blank=True, max_length=254, null=True)),
                ('hyperlink', models.CharField(
                    blank=True, max_length=254, null=True)),
                ('shape_leng', models.DecimalField(
                    blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('shape_area', models.DecimalField(
                    blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(
                    blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'cms_dengue',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Singapore',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('id_0', models.DecimalField(
                    blank=True, decimal_places=0, max_digits=10, null=True)),
                ('iso', models.CharField(blank=True, max_length=3, null=True)),
                ('name_0', models.CharField(
                    blank=True, max_length=75, null=True)),
                ('id_1', models.DecimalField(
                    blank=True, decimal_places=0, max_digits=10, null=True)),
                ('name_1', models.CharField(
                    blank=True, max_length=75, null=True)),
                ('hasc_1', models.CharField(
                    blank=True, max_length=15, null=True)),
                ('ccn_1', models.DecimalField(
                    blank=True, decimal_places=0, max_digits=10, null=True)),
                ('cca_1', models.CharField(
                    blank=True, max_length=254, null=True)),
                ('type_1', models.CharField(
                    blank=True, max_length=50, null=True)),
                ('engtype_1', models.CharField(
                    blank=True, max_length=50, null=True)),
                ('nl_name_1', models.CharField(
                    blank=True, max_length=50, null=True)),
                ('varname_1', models.CharField(
                    blank=True, max_length=150, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(
                    blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'cms_singapore',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                  parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
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
            name='CrisisTransactionLog',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_crisis', models.PositiveSmallIntegerField()),
                ('district', models.CharField(max_length=10)),
                ('date_recorded', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(blank=True, null=True,
                                            on_delete=django.db.models.deletion.CASCADE, to='cms.Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('district', models.CharField(
                    max_length=10, primary_key=True, serialize=False)),
                ('crisis', models.PositiveSmallIntegerField(default=0)),
                ('center', django.contrib.gis.db.models.fields.PointField(
                    blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isactive', models.BooleanField(default=True)),
                ('description', models.TextField(default=b'')),
                ('num_casualties', models.IntegerField(default=0)),
                ('num_injured', models.IntegerField(default=0)),
                ('date_recorded', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(
                    blank=True, srid=4326)),
                ('assistance_required', models.CharField(choices=[
                 (b'AMB', b'Ambulance'), (b'RES', b'Rescue'), (b'EVA', b'Evacuation')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EventTransactionLog',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[
                 (b'ED', b'Edit'), (b'CR', b'Create'), (b'DL', b'Delete')], max_length=2)),
                ('desc', models.CharField(blank=True, max_length=1024)),
                ('date_transaction', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(blank=True, null=True,
                                            on_delete=django.db.models.deletion.CASCADE, to='cms.Admin')),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='cms.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Haze',
            fields=[
                ('districtname', models.CharField(
                    max_length=128, primary_key=True, serialize=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(
                    srid=4326)),
                ('PSI', models.IntegerField(default=0)),
                ('PM25', models.IntegerField(default=0)),
                ('PM10', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                  parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
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
            name='Reporter',
            fields=[
                ('name', models.CharField(default=b'', max_length=128)),
                ('identification', models.CharField(
                    max_length=10, primary_key=True, serialize=False)),
                ('contact_number', models.CharField(blank=True, max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='TerroristEvent',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_hostiles', models.IntegerField(default=0)),
                ('attack_type', models.CharField(choices=[
                 (b'BMB', b'Bomb'), (b'BCH', b'Biochemical'), (b'HST', b'Hostage')], max_length=3)),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='cms.Event')),
            ],
        ),
        migrations.CreateModel(
            name='TrafficEvent',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_vehicles', models.IntegerField(default=0)),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='cms.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('districtname', models.CharField(
                    max_length=128, primary_key=True, serialize=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(
                    srid=4326)),
                ('condition', models.CharField(blank=True, max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='eventtransactionlog',
            name='operator',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Operator'),
        ),
        migrations.AddField(
            model_name='eventtransactionlog',
            name='reporter',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Reporter'),
        ),
        migrations.AddField(
            model_name='event',
            name='first_responder',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='first_responder', to='cms.Reporter'),
        ),
        migrations.AddField(
            model_name='event',
            name='operator',
            field=models.ManyToManyField(to='cms.Operator'),
        ),
        migrations.AddField(
            model_name='event',
            name='reporters',
            field=models.ManyToManyField(
                blank=True, related_name='other_responders', to='cms.Reporter'),
        ),
    ]
