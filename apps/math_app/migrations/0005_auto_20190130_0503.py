# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-30 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_app', '0004_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='admin_level',
        ),
        migrations.RemoveField(
            model_name='user',
            name='student_belongs_to',
        ),
        migrations.AddField(
            model_name='user',
            name='user_score_list',
            field=models.CharField(default=[], max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]