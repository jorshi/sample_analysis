# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-14 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0055_auto_20181213_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCAStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('window_length', models.IntegerField(blank=True, null=True)),
                ('window_start', models.IntegerField(blank=True, null=True)),
                ('dim_1_variance_ratio', models.FloatField(blank=True, null=True)),
                ('dim_2_variance_ratio', models.FloatField(blank=True, null=True)),
                ('dim_3_variance_ratio', models.FloatField(blank=True, null=True)),
                ('dim_4_variance_ratio', models.FloatField(blank=True, null=True)),
                ('variance_sum_2d', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='pcastats',
            unique_together=set([('window_length', 'window_start')]),
        ),
    ]
