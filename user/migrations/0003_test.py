# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-26 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20170226_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=12)),
                ('passwd', models.CharField(max_length=20, null=True)),
                ('sex', models.IntegerField(null=True)),
                ('birthday', models.CharField(max_length=20, null=True)),
                ('ctime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
