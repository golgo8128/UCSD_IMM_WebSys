# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWorkChunkPlanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkChunk_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
                ('type_note', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Work chunk class',
            },
        ),
        migrations.AlterModelOptions(
            name='workchunk_plan',
            options={'verbose_name': 'Plan for the work chunks', 'verbose_name_plural': 'Plans for the work chunks'},
        ),
        migrations.AlterModelOptions(
            name='workchunk_project',
            options={'verbose_name': 'Project for the work chunks', 'verbose_name_plural': 'Projects for the work chunks'},
        ),
        migrations.AlterModelOptions(
            name='workchunk_record',
            options={'verbose_name': 'Work record for the planned chunks', 'verbose_name_plural': 'Work records for the planned chunks'},
        ),
        migrations.AlterModelOptions(
            name='workchunk_served',
            options={'verbose_name': 'How the product was useful after work', 'verbose_name_plural': 'How the product was useful after work'},
        ),
        migrations.AlterModelOptions(
            name='workchunk_type',
            options={'verbose_name': 'Work chunk type'},
        ),
    ]
