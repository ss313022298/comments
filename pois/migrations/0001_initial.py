# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-07-03 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poi',
            fields=[
                ('poi_id', models.CharField(db_index=True, max_length=32, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='文章创建时间')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
    ]
