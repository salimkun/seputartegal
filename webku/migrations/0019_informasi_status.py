# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-04 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webku', '0018_remove_informasi_contents'),
    ]

    operations = [
        migrations.AddField(
            model_name='informasi',
            name='status',
            field=models.CharField(blank=True, choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], max_length=1, null=True),
        ),
    ]
