# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-29 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='alert',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='alert_msg',
            field=models.CharField(blank=True, default=True, max_length=300, null=True),
        ),
    ]
