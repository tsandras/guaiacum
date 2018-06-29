# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from editor.pages.admin import PageAdmin, TopicAdmin
from editor.pages.models import Page, Topic

from .models import (
    Attribute,
    AttributeLevel,
    AttributeDependency,
    Advantage,
    AttributeAdvantage,
    Label,
    Character,
    UserProfile
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
        'get_levels',
        'get_labels'
    )
    list_display_links = ('name',)
    ordering = ('name',)
    filter_horizontal = ('labels',)
    inlines = [AttributeDependencyInline, AttributeLevelInline]

    def get_labels(self, obj):
        return ", ".join([p.name for p in obj.labels.all()])

    def get_levels(self, obj):
        return ", ".join([str(p.level) for p in obj.levels.all().order_by('level')])


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
    inlines = [AttributeAdvantageInline]
    readonly_fields = ['tier', 'cost']
    filter_horizontal = ('conditions',)


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
    filter_horizontal = ('advantages',)
    ordering = ('first_name',)
    fields = ('first_name', 'last_name', 'nickname', 'owner', 'advantages', 'attribute_bonuses', 'total_pc', 'drawing', 'audio', 'image_tag')
    readonly_fields = ('image_tag',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'character'
    )
    ordering = ('user',)


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Advantage, AdvantageAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Character, CharactereAdmin)

admin.site.register(Page, PageAdmin)
admin.site.register(Topic, TopicAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
