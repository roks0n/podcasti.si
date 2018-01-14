# -*- coding: utf-8 -*-
from django.contrib import admin

from podcasts.models import Episode, Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    pass


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass
