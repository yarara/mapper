# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160413_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image_url',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='place',
            name='image_url',
            field=models.TextField(blank=True),
        ),
    ]