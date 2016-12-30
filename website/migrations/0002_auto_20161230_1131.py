# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-30 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='company_name',
            field=models.CharField(default='name', max_length=150, verbose_name='Raz\xf3n Social'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ctacte',
            name='date_1',
            field=models.DateField(null=True, verbose_name='Fecha Emision'),
        ),
        migrations.AlterField(
            model_name='ctacte',
            name='date_2',
            field=models.DateField(null=True, verbose_name='Fecha Vencimiento'),
        ),
    ]
