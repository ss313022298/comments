# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-07-05 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pois', '0003_auto_20180705_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poi',
            name='poi_id',
            field=models.CharField(db_index=True, default='ed9257547ff111e8be3f309c23a2312b', max_length=32, primary_key=True, serialize=False),
        ),
    ]
