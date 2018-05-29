# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models

from django.contrib.auth.models import User

from django.db.models import Max, Sum


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    short = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    tier = models.IntegerField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    conditions = models.ManyToManyField(
        'self', blank=True, through='AttributeDependency', related_name='condition_attributes', symmetrical=False
    )
    description = models.TextField(blank=True)
    reference = models.ForeignKey('self', blank=True, null=True, related_name='related_attributes')
    labels = models.ManyToManyField(Label, blank=True, related_name='label_attributes')

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
    bonuses = models.ManyToManyField(
        Attribute, blank=True, through='AttributeAdvantage', related_name='advantages', symmetrical=False
    )
    conditions = models.ManyToManyField('self', blank=True, related_name='are_required')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tier = 0
        self.cost = 0
        super().save(*args, **kwargs)
        if self.bonuses.all().aggregate(Max('tier'))['tier__max'] is not None:
            self.tier = self.bonuses.all().aggregate(Max('tier'))['tier__max']
        else:
            self.tier = 0
        if self.bonuses.all() is not None:
            for attribute_advantage in AttributeAdvantage.objects.filter(advantage_id=self.id):
                self.cost += attribute_advantage.attribute.cost * attribute_advantage.bonus * attribute_advantage.max
        else:
            self.cost = 0
        super().save(*args, **kwargs)


class AttributeAdvantage(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='advantage', null=True, blank=True)
    advantage = models.ForeignKey(Advantage, related_name='attribute', null=True, blank=True)
    bonus = models.IntegerField(default=1)
    max = models.IntegerField(default=1)
    become = models.IntegerField(blank=True, null=True)
    cost_limit = models.IntegerField(blank=True, null=True)
    label_limit = models.ForeignKey(Label, related_name='advantage', null=True, blank=True)


class Character(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    nickname = models.CharField(max_length=100, db_index=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, db_index=True, related_name='characters')
    advantages = models.ManyToManyField(Advantage, blank=True, related_name='advantages_characters')
    total_pc = models.IntegerField(default=100)


class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, db_index=True, related_name='profiles')
    character = models.ForeignKey(Character, null=True, blank=True)
