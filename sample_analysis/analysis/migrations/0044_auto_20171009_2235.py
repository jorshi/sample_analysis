# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-09 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0043_auto_20170526_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysispca',
            name='window_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analysispca',
            name='window_start',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='analysispca',
            unique_together=set([('sample', 'window_length', 'window_start')]),
        ),
    ]