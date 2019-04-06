from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from podcasts import serializers
from podcasts.models import Episode, Podcast
from podcasts.utils.images import get_thumbnail_url
from podcasts.utils.stats import track_episode, track_podcast
from podcasts.utils.time import pretty_date

from rest_framework import routers, viewsets


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse("")


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page")

        featured_podcasts = []
        featured = Podcast.objects.order_by("?")[:8]
        for podcast in featured:
            featured_podcasts.append(
                {
                    "slug": podcast.slug,
                    "image": get_thumbnail_url(podcast.image),
                    "name": podcast.name,
                }
            )
        latest_episodes = Episode.objects.exclude(
            published_datetime=None
        ).order_by("-published_datetime")
        paginator = Paginator(latest_episodes, settings.PAGE_SIZE)
        latest_episodes = paginator.get_page(page)

        episodes = []
        for episode in latest_episodes:
            episodes.append(
                {
                    "title": episode.title,
                    "podcast_name": episode.podcast.name,
                    "is_radio": episode.podcast.is_radio,
                    "published": pretty_date(episode.published_datetime),
                    "image": get_thumbnail_url(episode.podcast.image),
                    "slug": episode.slug,
                    "podcast_slug": episode.podcast.slug,
                    "external_url": episode.url,
                }
            )

        context.update(
            {
                "seo": {
                    "title": "Slovenski Podcasti - Največji seznam slovenskih podcastov",
                    "description": (
                        "Slovenski podcasti vsebuje največji seznam podcastov narejenih v "
                        "Sloveniji. Odkrij, spremljaj in poslušaj slovenske podcaste."
                    ),
                },
                "header": {
                    "url": "https://podcasti.si",
                    "title": "Slovenski Podcasti",
                    "subtitle": "Seznam vseh slovenskih podcastov",
                },
                "latest_episodes": episodes,
                "paginator": latest_episodes,
                "featured_podcasts": featured_podcasts,
            }
        )
        return context


class EpisodeView(TemplateView):
    template_name = "episode.html"

    def get_context_data(self, podcast_slug, episode_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = get_object_or_404(Podcast, slug=podcast_slug)
        episode = get_object_or_404(Episode, slug=episode_slug, podcast=podcast)

        track_episode(episode)
        track_podcast(podcast)

        context.update(
            {
                "seo": {
                    "title": "{} | podcasti.si".format(episode.title),
                    "description": episode.description,
                },
                "header": {
                    "url": "https://podcasti.si",
                    "title": "Slovenski Podcasti",
                    "subtitle": "Seznam vseh slovenskih podcastov",
                },
                "episode": episode,
            }
        )
        return context


class PodcastView(TemplateView):
    template_name = "podcast.html"

    def get_context_data(self, podcast_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = get_object_or_404(Podcast, slug=podcast_slug)

        track_podcast(podcast)

        page = self.request.GET.get("page")

        latest_episodes = podcast.episode_set.order_by("-published_datetime", "-created_datetime")
        paginator = Paginator(latest_episodes, settings.PAGE_SIZE)
        latest_episodes = paginator.get_page(page)

        episodes = []
        for episode in latest_episodes:
            episodes.append(
                {
                    "title": episode.title,
                    "podcast_name": episode.podcast.name,
                    "published": pretty_date(episode.published_datetime),
                    "slug": episode.slug,
                    "podcast_slug": episode.podcast.slug,
                    "external_url": episode.url,
                }
            )

        context.update(
            {
                "seo": {
                    "title": "{} Podcast | podcasti.si".format(podcast.name),
                    "description": podcast.description,
                },
                "header": {
                    "url": "https://podcasti.si",
                    "title": "Slovenski Podcasti",
                    "subtitle": "Seznam vseh slovenskih podcastov",
                },
                "podcast": podcast,
                "podcast_image": get_thumbnail_url(podcast.image),
                "episodes": episodes,
                "paginator": latest_episodes,
            }
        )
        return context


class AllPodcastsView(TemplateView):
    template_name = "all-podcasts.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        podcasts = Podcast.objects.order_by("name")

        context.update(
            {
                "seo": {
                    "title": "Seznam vseh slovenskih podcastov | podcasti.si",
                    "description": "Seznam vseh slovenskih podcastov na eni strani.",
                },
                "header": {
                    "url": "https://podcasti.si",
                    "title": "Slovenski Podcasti",
                    "subtitle": "Seznam vseh slovenskih podcastov",
                },
                "podcasts": podcasts,
            }
        )
        return context


class ApiEpisodes(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = Episode.objects.order_by("-published_datetime", "-created_datetime")
    serializer_class = serializers.EpisodeSerializer


class ApiPodcasts(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = Podcast.objects.order_by("name")
    serializer_class = serializers.PodcastSerializer


class ApiFeed(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = Episode.objects.prefetch_related("podcast").order_by(
        "-published_datetime", "-created_datetime"
    )
    serializer_class = serializers.FeedSerializer


router = routers.DefaultRouter()
router.register(r"episodes", ApiEpisodes, "episode")
router.register(r"podcasts", ApiPodcasts, "podcast")
router.register(r"feed", ApiFeed, "feed")
