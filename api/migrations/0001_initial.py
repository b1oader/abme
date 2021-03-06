# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-22 14:53
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(default='images/none/blank_article.jpg', upload_to='images/articles/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('year', models.IntegerField(choices=[(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)])),
                ('image', models.ImageField(default='images/none/blank_poster.jpg', upload_to='images/films/')),
                ('description', models.CharField(blank=True, default='Lorem ipsum dolor sit amet,\n    consectetur adipiscing elit. Etiam maximus efficitur lacus, sit amet pretium lorem \n    iaculis id. Nulla hendrerit risus at justo imperdiet, eget sagittis felis consequat. \n    Ut tempor luctus felis id ullamcorper. Ut fringilla pharetra magna a scelerisque.\n    Maecenas nec sem varius mi rhoncus scelerisque sed sed enim. Suspendisse\n    blandit ante at ipsum feugiat, vitae ultrices enim blandit.', max_length=500)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filmcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('biography', models.CharField(default='Lorem ipsum dolor sit amet,\n    consectetur adipiscing elit. Etiam maximus efficitur lacus, sit amet pretium lorem \n    iaculis id. Nulla hendrerit risus at justo imperdiet, eget sagittis felis consequat. \n    Ut tempor luctus felis id ullamcorper. Ut fringilla pharetra magna a scelerisque.\n    Maecenas nec sem varius mi rhoncus scelerisque sed sed enim. Suspendisse\n    blandit ante at ipsum feugiat, vitae ultrices enim blandit.', max_length=500)),
                ('photo', models.ImageField(default='photos/none/default.png', upload_to='photos/persons/')),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('year', models.IntegerField(choices=[(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)])),
                ('image', models.ImageField(default='images/none/blank_poster.jpg', upload_to='images/serials/')),
                ('seasons', models.PositiveSmallIntegerField(default=1)),
                ('description', models.CharField(blank=True, default='Lorem ipsum dolor sit amet,\n    consectetur adipiscing elit. Etiam maximus efficitur lacus, sit amet pretium lorem \n    iaculis id. Nulla hendrerit risus at justo imperdiet, eget sagittis felis consequat. \n    Ut tempor luctus felis id ullamcorper. Ut fringilla pharetra magna a scelerisque.\n    Maecenas nec sem varius mi rhoncus scelerisque sed sed enim. Suspendisse\n    blandit ante at ipsum feugiat, vitae ultrices enim blandit.', max_length=500)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Serialcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person')),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Serial')),
            ],
        ),
        migrations.AddField(
            model_name='serial',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='serial_actors', through='api.Serialcast', to='api.Person'),
        ),
        migrations.AddField(
            model_name='serial',
            name='category',
            field=models.ManyToManyField(blank=True, to='api.Category'),
        ),
        migrations.AddField(
            model_name='serial',
            name='creators',
            field=models.ManyToManyField(blank=True, related_name='serial_creators', to='api.Person'),
        ),
        migrations.AddField(
            model_name='filmcast',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person'),
        ),
        migrations.AddField(
            model_name='filmcast',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Film'),
        ),
        migrations.AddField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='film_actors', through='api.Filmcast', to='api.Person'),
        ),
        migrations.AddField(
            model_name='film',
            name='category',
            field=models.ManyToManyField(blank=True, to='api.Category'),
        ),
        migrations.AddField(
            model_name='film',
            name='directors',
            field=models.ManyToManyField(blank=True, related_name='film_directors', to='api.Person'),
        ),
        migrations.AddField(
            model_name='film',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='film_writers', to='api.Person'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(blank=True, to='api.ArticleCategory'),
        ),
    ]
