# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 19:41
from __future__ import unicode_literals

import applications.rooms.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='no_of_beds',
            field=models.IntegerField(validators=[applications.rooms.models.no_of_beds_validator]),
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(unique=True, validators=[applications.rooms.models.room_number_validator]),
        ),
    ]
