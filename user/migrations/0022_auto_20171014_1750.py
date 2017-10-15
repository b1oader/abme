# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-14 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171012_2052'),
        ('user', '0021_group_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bread',
        ),
        migrations.AddField(
            model_name='profile',
            name='film',
            field=models.ManyToManyField(to='api.Film'),
        ),
        migrations.DeleteModel(
            name='Bread',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]