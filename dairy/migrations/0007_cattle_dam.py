# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairy', '0006_auto_20171013_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='cattle',
            name='dam',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
