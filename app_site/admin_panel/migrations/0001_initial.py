# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 13:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(max_length=100)),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Occupied from')),
                ('end_date', models.DateField(default=datetime.date.today, verbose_name='Occupied to')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.City')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Occupied from')),
                ('end_date', models.DateField(default=datetime.date.today, verbose_name='Occupied to')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.Client')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.Object')),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='reservations',
            field=models.ManyToManyField(through='admin_panel.Reservation', to='admin_panel.Client'),
        ),
    ]
