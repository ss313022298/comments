# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-07-04 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pois', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poi',
            name='poi_content',
            field=models.CharField(default='文章内容为空', max_length=1000),
        ),
        migrations.AddField(
            model_name='poi',
            name='poi_title',
            field=models.CharField(default='文章标题为空', max_length=20),
        ),
        migrations.AlterField(
            model_name='poi',
            name='poi_id',
            field=models.CharField(db_index=True, default='ee8b3fce7f5911e8be3f309c23a2312b', max_length=32, primary_key=True, serialize=False),
        ),
    ]
