# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-18 21:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0038_auto_20170518_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysisfull',
            name='lat_dev',
        ),
        migrations.RemoveField(
            model_name='analysisfull',
            name='rms_dev',
        ),
        migrations.RemoveField(
            model_name='analysisfull',
            name='temporal_centroid_dev',
        ),
    ]
