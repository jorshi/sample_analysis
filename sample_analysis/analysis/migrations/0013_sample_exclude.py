# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0012_analysis_onset'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='exclude',
            field=models.BooleanField(default=False),
        ),
    ]