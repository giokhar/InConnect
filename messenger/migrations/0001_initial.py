# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-03 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('type', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'suggestions',
            },
        ),
    ]