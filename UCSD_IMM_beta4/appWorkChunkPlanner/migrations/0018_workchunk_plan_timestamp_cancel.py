# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWorkChunkPlanner', '0017_workchunk_plan_plan_cancel_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='workchunk_plan',
            name='timestamp_cancel',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Canceled time'),
        ),
    ]