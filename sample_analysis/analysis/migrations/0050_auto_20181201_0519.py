# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-01 05:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0049_auto_20181201_0444'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='manifold',
            unique_together=set([('sample', 'window_length', 'window_start', 'method')]),
        ),
    ]