# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-01 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0045_auto_20171009_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisTSNE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('window_length', models.IntegerField(blank=True, null=True)),
                ('window_start', models.IntegerField(blank=True, null=True)),
                ('dim_1', models.FloatField(blank=True, null=True)),
                ('dim_2', models.FloatField(blank=True, null=True)),
                ('dim_3', models.FloatField(blank=True, null=True)),
                ('dim_4', models.FloatField(blank=True, null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.Sample')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='analysistsne',
            unique_together=set([('sample', 'window_length', 'window_start')]),
        ),
    ]
