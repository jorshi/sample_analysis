# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-14 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0019_samplepack_info_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisZ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loudness', models.FloatField(blank=True, null=True)),
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
    ]
