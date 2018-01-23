from django.contrib import sitemaps
from django.urls import reverse

from podcasts.models import Episode, Podcast


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class PodcastsSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Podcast.objects.all()

    def lastmod(self, obj):
        return obj.created_datetime

    def location(self, obj):
        return reverse(
            'podcast', kwargs={'podcast_slug': obj.slug}
        )


class EpisodesSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Episode.objects.all()

    def lastmod(self, obj):
        return obj.created_datetime

    def location(self, obj):
        return reverse(
            'episode', kwargs={'podcast_slug': obj.podcast.slug, 'episode_slug': obj.slug}
        )


sitemaps_dict = {
    'static': StaticViewSitemap,
    'episodes': EpisodesSitemap,
    'podcasts': PodcastsSitemap,
}
