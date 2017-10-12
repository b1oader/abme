# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_film_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default='images/none/blank_poster.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='film',
            name='image',
            field=models.ImageField(default='images/none/blank_poster.jpg', upload_to='images/'),
        ),
    ]
