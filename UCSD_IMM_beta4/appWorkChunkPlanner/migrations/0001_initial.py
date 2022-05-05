# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkChunk_Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Planned time')),
                ('plan_note', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='WorkChunk_Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_name', models.CharField(max_length=100)),
                ('proj_note', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='WorkChunk_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Recorded time')),
                ('start_time', models.DateTimeField(verbose_name='Started time')),
                ('end_time', models.DateTimeField(verbose_name='Ended time')),
                ('weight_per_time', models.FloatField(default=1.0)),
                ('rec_note', models.TextField(default='')),
                ('corresp_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appWorkChunkPlanner.WorkChunk_Plan')),
            ],
        ),
        migrations.CreateModel(
            name='WorkChunk_Served',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Recorded time')),
                ('score', models.IntegerField(default=70)),
                ('served_note', models.TextField(default='')),
                ('worked_chunk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appWorkChunkPlanner.WorkChunk_Record')),
            ],
        ),
        migrations.CreateModel(
            name='WorkChunk_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
                ('type_note', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='workchunk_plan',
            name='chunk_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appWorkChunkPlanner.WorkChunk_Type'),
        ),
        migrations.AddField(
            model_name='workchunk_plan',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='workchunk_plan',
            name='proj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appWorkChunkPlanner.WorkChunk_Project'),
        ),
    ]
