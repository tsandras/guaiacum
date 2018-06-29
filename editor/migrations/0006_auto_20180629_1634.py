# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-29 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0005_auto_20180629_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advantage',
            name='conditions',
            field=models.ManyToManyField(blank=True, related_name='are_required', to='editor.Advantage'),
        ),
        migrations.AlterField(
            model_name='character',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audio/characters/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='drawing',
            field=models.ImageField(blank=True, null=True, upload_to='drawing/characters/'),
        ),
        migrations.AlterField(
            model_name='page',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audio/pages/'),
        ),
        migrations.AlterField(
            model_name='page',
            name='drawing',
            field=models.ImageField(blank=True, null=True, upload_to='drawing/pages/'),
        ),
        migrations.AlterField(
            model_name='section',
            name='drawing',
            field=models.FileField(blank=True, null=True, upload_to='drawing/sections/'),
        ),
    ]
