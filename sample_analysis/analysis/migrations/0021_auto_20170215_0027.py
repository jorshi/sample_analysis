# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0020_analysisz'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='duration',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analysisz',
            name='duration',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
