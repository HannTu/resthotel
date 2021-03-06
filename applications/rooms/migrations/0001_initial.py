# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('no_of_beds', models.IntegerField()),
                ('bathroom_inside', models.BooleanField()),
                ('standard', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
            ],
        ),
    ]
