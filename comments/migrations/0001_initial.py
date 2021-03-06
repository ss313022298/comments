# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-07-04 07:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion




class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0003_auto_20180704_0714'),
        ('pois', '0002_auto_20180704_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoiComment',
            fields=[
                ('content', models.TextField(max_length=500, verbose_name='评论')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('comment_id', models.CharField(db_index=True, max_length=32, primary_key=True, serialize=False)),
                ('poi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pois.Poi', verbose_name='评论所属文章')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tags.Tag', verbose_name='评论所属标签')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='PoiCommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='评论')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comments.PoiComment', verbose_name='一级评论', )),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.PoiCommentReply', verbose_name='回复对象', )),
            ],
            options={
                'ordering': ['create_time'],
            },
        ),
    ]
