# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-26 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20160926_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='x',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='graph',
            name='y',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
