# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-06-22 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0037_auto_20170505_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_commercial',
            field=models.BooleanField(default=False, verbose_name='Es Comercial?'),
        ),
    ]
