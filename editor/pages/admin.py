from django.contrib import admin

from .models import Section


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0


class PageAdmin(admin.ModelAdmin):

    ordering = ('name',)
    filter_horizontal = ('topics',)
    inlines = [SectionInline]


class TopicAdmin(admin.ModelAdmin):

    ordering = ('name',)
