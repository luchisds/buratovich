# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-26 23:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_userinfo_old_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='old_user',
        ),
    ]
