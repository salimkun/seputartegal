# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-04 13:43
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webku', '0014_remove_informasi_kategori'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('images', models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
    ]
