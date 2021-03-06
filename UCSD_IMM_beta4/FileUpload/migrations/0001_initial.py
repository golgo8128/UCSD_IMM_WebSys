# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 23:06
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
            name='DataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatype', models.CharField(max_length=100, unique=True, verbose_name='Data type')),
            ],
        ),
        migrations.CreateModel(
            name='FileUploaded',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifile', models.FileField(max_length=500, upload_to='/Users/rsaito/Sites/WebSys_UCSD2/UCSD_IMM_beta4/UCSD_IMM_WorkSpace/FilesUploaded/Ver0p1/%Y/%m/%d', verbose_name='Uploaded file')),
                ('idescription', models.CharField(max_length=2000, verbose_name='Brief file description')),
                ('ifilename', models.CharField(max_length=500, verbose_name='Original file name')),
                ('itimestamp', models.DateTimeField(verbose_name='Time uploaded')),
                ('idatatype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileUpload.DataType', verbose_name='Data type')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projname', models.CharField(max_length=100, unique=True, verbose_name='Project name')),
            ],
        ),
        migrations.AddField(
            model_name='fileuploaded',
            name='iproj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileUpload.Project', verbose_name='Project name'),
        ),
        migrations.AddField(
            model_name='fileuploaded',
            name='iuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uploaded user'),
        ),
    ]
