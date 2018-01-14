# -*- coding: utf-8 -*-
from django.db import models


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ImageField()
    website = models.CharField(max_length=256)
    authors = models.CharField(max_length=30)


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ImageField()
