# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-23 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0029_auto_20170223_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='pcacomponents',
            name='dimension',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
