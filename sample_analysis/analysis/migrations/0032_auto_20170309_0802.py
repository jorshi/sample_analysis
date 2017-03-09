# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0031_auto_20170304_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysispca',
            name='components',
        ),
        migrations.RemoveField(
            model_name='analysispca',
            name='dim_10',
        ),
        migrations.RemoveField(
            model_name='analysispca',
            name='dim_9',
        ),
        migrations.RemoveField(
            model_name='analysispca',
            name='variance',
        ),
        migrations.DeleteModel(
            name='PCAComponents',
        ),
        migrations.DeleteModel(
            name='PCAVariance',
        ),
    ]
