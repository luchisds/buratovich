# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-28 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_userinfo_account_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='random_password',
            field=models.BooleanField(default=True),
        ),
    ]
