# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWorkChunkPlanner', '0006_workchunk_plan_plan_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workchunk_plan',
            name='plan_note',
            field=models.TextField(blank=True, default=''),
        ),
    ]
