# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-13 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0051_auto_20181212_2211'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnalysisPCA',
            new_name='PCA',
        ),
    ]
