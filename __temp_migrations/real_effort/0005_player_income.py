# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-23 03:15
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('real_effort', '0004_auto_20180522_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='income',
            field=otree.db.models.IntegerField(null=True),
        ),
    ]