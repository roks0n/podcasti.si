# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    website = models.URLField(max_length=256, blank=True, null=True)
    authors = models.CharField(max_length=256, blank=True, null=True)
    feed_url = models.URLField(max_length=256)
    last_sync = models.DateTimeField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Podcast "{}">'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField()
    published_datetime = models.DateTimeField()
    audio = models.URLField(max_length=256, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} from "{}"'.format(self.title, self.podcast.name)

    def __repr__(self):
        return '<Episode "{}" from "{}">'.format(self.title, self.podcast.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Stats(models.Model):
    day = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=1)
    payload = JSONField(default=dict)

    def __str__(self):
        return '{} on "{}"'.format(self.payload['type'], self.day)

    def __repr__(self):
        return '<Stats "{}" on "{}">'.format(self.payload['type'], self.day)
