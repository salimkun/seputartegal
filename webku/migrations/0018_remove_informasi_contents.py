# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-04 20:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webku', '0017_auto_20160904_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informasi',
            name='contents',
        ),
    ]