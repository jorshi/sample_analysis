# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-13 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0054_auto_20181213_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifold',
            name='method',
            field=models.CharField(choices=[('tsne', 'TSNE'), ('isomap', 'Isomap'), ('locally_linear', 'Locally Linear'), ('mds', 'MDS'), ('spectral', 'Spectral')], default='tsne', max_length=20),
        ),
    ]
