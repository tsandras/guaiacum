# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from .models import (
    Attribute,
    AttributeLevel,
    AttributeDependency,
    Advantage,
    AttributeAdvantage,
    Label,
    Character
)


class AttributeLevelInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':90})},
    }
    model = AttributeLevel
    extra = 0


class AttributeDependencyInline(admin.StackedInline):
    model = AttributeDependency
    fk_name = 'condition'
    extra = 0


class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tier',
        'cost',
    )
    list_display_links = ('name',)
    ordering = ('name',)
    filter_horizontal = ('conditions',)
    inlines = [AttributeDependencyInline, AttributeLevelInline]


class AttributeAdvantageInline(admin.StackedInline):
    model = AttributeAdvantage
    extra = 0


class AdvantageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tier',
        'cost',
    )
    list_display_links = ('name',)
    ordering = ('name',)
    filter_horizontal = ('conditions',)
    inlines = [AttributeAdvantageInline]
    readonly_fields = ['tier', 'cost']


class LabelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'short'
    )
    list_display_links = ('name',)
    ordering = ('name',)


class CharactereAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name'
    )
    list_display_links = ('first_name',)
    ordering = ('first_name',)


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Advantage, AdvantageAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Character, CharactereAdmin)
