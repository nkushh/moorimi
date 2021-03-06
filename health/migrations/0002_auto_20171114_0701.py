# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 07:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dairy', '0009_cattle_sale'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dewormed_animals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.Cattle')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduled_deworming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment', models.TextField()),
                ('result', models.CharField(blank=True, max_length=200)),
                ('vet', models.CharField(blank=True, max_length=200)),
                ('cost', models.FloatField()),
                ('remarks', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('account', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='health_record',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='health_record',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='health_record',
            name='result',
        ),
        migrations.RemoveField(
            model_name='health_record',
            name='treatment',
        ),
        migrations.RemoveField(
            model_name='health_record',
            name='vet',
        ),
        migrations.AddField(
            model_name='treatment',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.Health_record'),
        ),
        migrations.AddField(
            model_name='dewormed_animals',
            name='deworming_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.Scheduled_deworming'),
        ),
    ]
