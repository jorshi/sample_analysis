# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-14 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0057_auto_20181214_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='pcastat',
            name='sample_type',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='pcastat',
            unique_together=set([('sample_type', 'window_length', 'window_start')]),
        ),
    ]