# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webku', '0011_auto_20160821_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='keterangan',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='berita',
            name='sumber',
            field=models.CharField(blank=True, choices=[('SuaraMerdeka.com', 'SuaraMerdeka'), ('RadarTegal.com', 'RadarTegal')], max_length=40, null=True),
        ),
    ]
