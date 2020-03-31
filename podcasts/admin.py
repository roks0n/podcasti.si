from django.contrib import admin

from podcasts.models import Category, Episode, Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    search_fields = ("name", "authors")


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
