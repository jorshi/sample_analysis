# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-14 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0018_auto_20170214_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplepack',
            name='info_link',
            field=models.URLField(blank=True, default=None),
        ),
    ]
