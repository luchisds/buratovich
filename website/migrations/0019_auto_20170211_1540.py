# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-11 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20170211_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='date',
            field=models.DateField(verbose_name='Fecha'),
        ),
    ]
