# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-26 02:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0042_analysisfull_window_start'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='analysisfull',
            unique_together=set([('sample', 'window_length', 'window_start')]),
        ),
    ]
