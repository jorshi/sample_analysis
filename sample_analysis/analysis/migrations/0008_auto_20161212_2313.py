# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_auto_20161212_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='loudness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='spectral_flux',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
