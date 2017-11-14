# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 06:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dairy', '0009_cattle_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Health_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.TextField()),
                ('diagnosis', models.CharField(max_length=200)),
                ('treatment', models.TextField()),
                ('result', models.CharField(max_length=200)),
                ('vet', models.CharField(max_length=200)),
                ('cost', models.FloatField()),
                ('remarks', models.TextField()),
                ('treatment_date', models.DateField()),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.Cattle')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccinate_schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine', models.CharField(max_length=200)),
                ('scheduled_date', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccinated_animals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.Cattle')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.Vaccinate_schedule')),
            ],
        ),
    ]