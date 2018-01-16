# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    website = models.URLField(max_length=256, blank=True, null=True)
    authors = models.CharField(max_length=30, blank=True, null=True)
    feed_url = models.URLField(max_length=256)
    last_sync = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'Podcast "{}"'.format(self.name)

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

    def __str__(self):
        return 'Episode "{}" from "{}"'.format(self.title, self.podcast.name)

    def __repr__(self):
        return '<Episode "{}" from "{}">'.format(self.title, self.podcast.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
