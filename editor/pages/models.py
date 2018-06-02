from django.db import models
from editor.models import Attribute


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    short = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='pages')
    quote = models.TextField(blank=True)
    drawing = models.FileField(upload_to='media/drawing/pages/', blank=True, null=True)
    audio = models.FileField(upload_to='media/audio/pages/', blank=True, null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    page = models.ForeignKey(Page, blank=True, null=True, related_name='sections')
    attribute = models.ForeignKey(Attribute, blank=True, null=True, related_name='sections')
    level = models.IntegerField(default=1)
    quote = models.TextField(blank=True)
    drawing = models.FileField(upload_to='media/drawing/sections/', storage=OverwriteStorage(), blank=True, null=True)