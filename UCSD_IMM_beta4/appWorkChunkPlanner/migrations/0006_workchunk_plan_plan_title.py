# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWorkChunkPlanner', '0005_auto_20160215_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='workchunk_plan',
            name='plan_title',
            field=models.CharField(default='No title', max_length=100),
            preserve_default=False,
        ),
    ]
