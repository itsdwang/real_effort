# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-23 04:12
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('real_effort', '0006_player_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='contribution',
            field=otree.db.models.IntegerField(default=-1, null=True),
        ),
    ]