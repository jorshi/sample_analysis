# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-04 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0030_pcacomponents_dimension'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisMinMax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equal_loudness', models.FloatField(blank=True, null=True)),
                ('spectral_centroid', models.FloatField(blank=True, null=True)),
                ('spectral_centroid_1', models.FloatField(blank=True, null=True)),
                ('spectral_centroid_2', models.FloatField(blank=True, null=True)),
                ('temporal_centroid', models.FloatField(blank=True, null=True)),
                ('rms', models.FloatField(blank=True, null=True)),
                ('spectral_kurtosis', models.FloatField(blank=True, null=True)),
                ('pitch_salience', models.FloatField(blank=True, null=True)),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analysis.Sample')),
            ],
        ),
        migrations.RemoveField(
            model_name='analysisrobustscale',
            name='sample',
        ),
        migrations.DeleteModel(
            name='AnalysisRobustScale',
        ),
    ]
