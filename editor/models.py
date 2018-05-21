# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models

from django.db.models import Max, Sum


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
        'Attribute', blank=True, through='AttributeAdvantage', related_name='advantages', symmetrical=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.conditions.all().aggregate(Max('tier'))['tier__max'] is not None:
            self.tier = self.conditions.all().aggregate(Max('tier'))['tier__max']
        else:
            self.tier = 1
        if self.conditions.all().aggregate(Sum('cost'))['cost__sum'] is not None:
            self.cost = self.conditions.all().aggregate(Sum('cost'))['cost__sum']
        else:
            self.cost = 1
        super().save(*args, **kwargs)


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    short = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name


class AttributeAdvantage(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='advantage', null=True, blank=True)
    advantage = models.ForeignKey(Advantage, related_name='attribute', null=True, blank=True)
    mod = models.IntegerField(default=1)
    max = models.IntegerField(default=0)
    cost_limit = models.IntegerField(blank=True, null=True)
    label_limit = models.ForeignKey(Label, related_name='advantage', null=True, blank=True)


class Character(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    nickname = models.CharField(max_length=100, db_index=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, db_index=True, related_name='characters')
    advantages = models.ManyToManyField('Advantage', blank=True, related_name='advantages_characters')
    pc = models.IntegerField(default=50)
    px = models.IntegerField(default=0)
