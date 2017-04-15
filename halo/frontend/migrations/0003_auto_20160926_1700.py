# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-26 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_query_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.Query')),
            ],
        ),
        migrations.AddField(
            model_name='database',
            name='host_and_port',
            field=models.TextField(default='localhost:5672', null=True),
        ),
    ]
