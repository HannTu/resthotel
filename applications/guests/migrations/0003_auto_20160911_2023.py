# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 20:23
from __future__ import unicode_literals

import applications.guests.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0002_auto_20160911_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='pesel',
            field=models.IntegerField(unique=True, validators=[applications.guests.models.pesel_length_validator]),
        ),
    ]