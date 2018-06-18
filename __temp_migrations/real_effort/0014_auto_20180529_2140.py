# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-30 04:40
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('real_effort', '0013_auto_20180529_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='transcription',
        ),
        migrations.AddField(
            model_name='player',
            name='transcriptionDone',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')]),
        ),
    ]