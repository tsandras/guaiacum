# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from operator import attrgetter


class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    tier = models.IntegerField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    conditions = models.ManyToManyField(
        'self', blank=True, through='AttributeDependency', related_name='condition_attributes', symmetrical=False
    )
    description = models.TextField(blank=True)
    reference = models.ForeignKey('self', blank=True, null=True, related_name='related_attributes')
    labels = models.ManyToManyField('Label', blank=True, related_name='label_attributes')

    def __str__(self):
        return self.name


class AttributeDependency(models.Model):
    condition = models.ForeignKey(Attribute, related_name='attribute')
    attribute = models.ForeignKey(Attribute, related_name='condition')
    level = models.IntegerField(default=1)


class AttributeLevel(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='levels')
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=True)
    level = models.IntegerField(blank=False, null=False)


class Advantage(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    tier = models.IntegerField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=True)
    conditions = models.ManyToManyField(
        'Attribute', blank=True, through='AttributeAdvantage', related_name='advantages'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tier = max(self.objects.conditions, key=attrgetter('tier'))
        self.cost = sum(self.objects.conditions, key=attrgetter('cost'))
        super().save(*args, **kwargs)


class AttributeAdvantage(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='advantage')
    advantage = models.ForeignKey(Advantage, related_name='attribute')
    mod = models.IntegerField(default=1)
    max = models.IntegerField(default=0)


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    short = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name
