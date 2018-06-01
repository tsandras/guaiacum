from django.contrib import admin
from django.forms.models import ModelMultipleChoiceField

from .models import Section, Topic


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0


class PageAdmin(admin.ModelAdmin):

    ordering = ('name',)
    filter_horizontal = ('topics',)
    inlines = [SectionInline]

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(PageAdmin, self).get_form(request, obj, **kwargs)
    #     # form.base_fields['name'].initial = 'test'
    #     return form


class TopicAdmin(admin.ModelAdmin):

    ordering = ('name',)
