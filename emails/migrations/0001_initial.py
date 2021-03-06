# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0009_auto_20170827_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSendingFact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
            ],
            options={
                'verbose_name': 'Отправленый имейл',
                'verbose_name_plural': 'Отправленые имейлы',
            },
        ),
        migrations.CreateModel(
            name='EmailType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Тип имейла',
                'verbose_name_plural': 'Типы имейлов',
            },
        ),
        migrations.AddField(
            model_name='emailsendingfact',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.EmailType'),
        ),
    ]
