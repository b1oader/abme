# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-20 21:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20180120_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
    ]