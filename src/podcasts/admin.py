from django.contrib import admin

from podcasts.models import Episode, Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ('name', 'authors',)


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ('title',)
