# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 11:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dairy', '0005_auto_20171013_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='milk',
            old_name='cow',
            new_name='cattle',
        ),
    ]
