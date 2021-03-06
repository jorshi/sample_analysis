# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-23 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0025_remove_analysis_loudness'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dim_1', models.FloatField(blank=True, null=True)),
                ('dim_2', models.FloatField(blank=True, null=True)),
                ('dim_3', models.FloatField(blank=True, null=True)),
                ('dim_4', models.FloatField(blank=True, null=True)),
                ('dim_5', models.FloatField(blank=True, null=True)),
                ('dim_6', models.FloatField(blank=True, null=True)),
                ('dim_7', models.FloatField(blank=True, null=True)),
                ('dim_8', models.FloatField(blank=True, null=True)),
                ('dim_9', models.FloatField(blank=True, null=True)),
                ('dim_10', models.FloatField(blank=True, null=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analysis.Sample')),
            ],
        ),
    ]
