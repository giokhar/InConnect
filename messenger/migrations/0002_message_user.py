# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-03 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(max_length=30, primary_key=True, serialize=False)),
                ('chat_id', models.IntegerField(unique=True)),
                ('sender_one', models.CharField(max_length=255)),
                ('sender_two', models.CharField(max_length=255)),
                ('message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'messages',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False)),
                ('sender_id', models.CharField(max_length=255)),
                ('topic', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
