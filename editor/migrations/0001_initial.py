# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-28 06:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advantage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('tier', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('tier', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeAdvantage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.IntegerField(default=1)),
                ('become', models.IntegerField(blank=True, null=True)),
                ('cost_limit', models.IntegerField(blank=True, null=True)),
                ('advantage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='editor.Advantage')),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advantage', to='editor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='condition', to='editor.Attribute')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='editor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('level', models.IntegerField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='editor.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_index=True, max_length=100)),
                ('last_name', models.CharField(db_index=True, max_length=100)),
                ('nickname', models.CharField(db_index=True, max_length=100)),
                ('total_pc', models.IntegerField(default=100)),
                ('advantages', models.ManyToManyField(blank=True, related_name='advantages_characters', to='editor.Advantage')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('short', models.CharField(db_index=True, max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('level', models.IntegerField(default=1)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='editor.Attribute')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='editor.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('short', models.CharField(db_index=True, max_length=10, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='pages', to='editor.Topic'),
        ),
        migrations.AddField(
            model_name='attributeadvantage',
            name='label_limit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advantage', to='editor.Label'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='conditions',
            field=models.ManyToManyField(blank=True, related_name='condition_attributes', through='editor.AttributeDependency', to='editor.Attribute'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='label_attributes', to='editor.Label'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_attributes', to='editor.Attribute'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='bonuses',
            field=models.ManyToManyField(blank=True, related_name='advantages', through='editor.AttributeAdvantage', to='editor.Attribute'),
        ),
        migrations.AddField(
            model_name='advantage',
            name='conditions',
            field=models.ManyToManyField(blank=True, null=True, related_name='_advantage_conditions_+', to='editor.Advantage'),
        ),
    ]
