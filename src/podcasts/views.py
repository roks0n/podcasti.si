from datetime import datetime, timedelta

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from podcasts import serializers
from podcasts.models import Episode, Podcast
from podcasts.utils.categories import (
    CATEGORIES_TRANSLATIONS,
    EPISODE_CATEGORIES_TO_SLUGS,
    EPISODE_SLUGS_TO_CATEGORIES,
)
from podcasts.utils.images import get_thumbnail_url
from podcasts.utils.stats import track_episode, track_podcast
from podcasts.utils.time import pretty_date
from podcasts.utils.logger import get_log

from rest_framework import routers, viewsets

log = get_log(__name__)


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
        filter_by = self.request.GET.get("filter_by", None)

        featured_podcasts = []

        latest_episodes = (
            Episode.objects.exclude(published_datetime=None)
            .filter(published_datetime__gte=datetime.now() - timedelta(days=30))
            .values("podcast__id")
            .distinct()
        )
        featured = Podcast.objects.filter(id__in=latest_episodes).order_by("?")[:8]
        for podcast in featured:
            featured_podcasts.append(
                {
                    "slug": podcast.slug,
                    "image": get_thumbnail_url(podcast.image),
                    "name": podcast.name,
                }
            )

        latest_episodes = (
            # exclude here is temp - so we don't have these entries on the top
            Episode.objects.exclude(published_datetime=None).order_by("-published_datetime")
        )

        if filter_by in ["radio", "indie"]:
            if filter_by == "radio":
                latest_episodes = latest_episodes.filter(podcast__is_radio=True)
            else:
                latest_episodes = latest_episodes.filter(
                    Q(podcast__is_radio=False) | Q(podcast__is_radio=None)
                )

        paginator = Paginator(latest_episodes, settings.PAGE_SIZE)
        latest_episodes = paginator.get_page(page)
        episodes = []
        for episode in latest_episodes:
            podcast_category = None
            category_slug = None
            if episode.podcast.category:
                podcast_category = CATEGORIES_TRANSLATIONS.get(episode.podcast.category.name)
                category_slug = EPISODE_CATEGORIES_TO_SLUGS.get(episode.podcast.category.name)

            episodes.append(
                {
                    "id": episode.id,
                    "title": episode.title,
                    "podcast_name": episode.podcast.name,
                    "is_radio": episode.podcast.is_radio,
                    "published": pretty_date(episode.published_datetime),
                    "image": get_thumbnail_url(episode.podcast.image),
                    "slug": episode.slug,
                    "podcast_slug": episode.podcast.slug,
                    "podcast_category": podcast_category,
                    "category_slug": category_slug,
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
                "title": "Najnovejše epizode",
                "latest_episodes": episodes,
                "paginator": latest_episodes,
                "featured_podcasts": featured_podcasts,
                "filter_by": filter_by,
                "is_staff": self.request.user.is_staff,
            }
        )
        return context


class EpisodeView(TemplateView):
    template_name = "episode.html"

    def get_context_data(self, podcast_slug, episode_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        episode_qs = Episode.objects.filter(slug=episode_slug, podcast=podcast)
        if not episode_qs.exists():
            raise Http404
        
        if episode_qs.count() > 1:
            log.warning(f"{episode_slug} has ({episode_qs.count()}) duplicated episodes!")
            episode = episode.last()
        else:
            episode = episode_qs.get()

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

        episodes = podcast.episode_set.order_by("-published_datetime", "-created_datetime")
        paginator = Paginator(episodes, settings.PAGE_SIZE)
        latest_episodes = paginator.get_page(page)

        episodes = []
        for episode in latest_episodes:
            episodes.append(
                {
                    "id": episode.id,
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
                "episodes_feed": latest_episodes[:10],
                "paginator": latest_episodes,
                "is_staff": self.request.user.is_staff,
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


class EpisodeCategoryView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, category_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        category = EPISODE_SLUGS_TO_CATEGORIES.get(f"{category_slug}")
        if not category:
            raise Http404

        category_i18n = CATEGORIES_TRANSLATIONS.get(category)

        page = self.request.GET.get("page")
        filter_by = self.request.GET.get("filter_by", None)

        latest_episodes = (
            Episode.objects.filter(podcast__category__name=category)
            .exclude(podcast__category=None)
            .exclude(published_datetime=None)  # temp - so we don't have these entries on the top
            .order_by("-published_datetime")
        )

        if filter_by in ["radio", "indie"]:
            if filter_by == "radio":
                latest_episodes = latest_episodes.filter(podcast__is_radio=True)
            else:
                latest_episodes = latest_episodes.filter(
                    Q(podcast__is_radio=False) | Q(podcast__is_radio=None)
                )

        paginator = Paginator(latest_episodes, settings.PAGE_SIZE)
        latest_episodes = paginator.get_page(page)
        episodes = []
        for episode in latest_episodes:
            episodes.append(
                {
                    "id": episode.id,
                    "title": episode.title,
                    "podcast_name": episode.podcast.name,
                    "is_radio": episode.podcast.is_radio,
                    "published": pretty_date(episode.published_datetime),
                    "image": get_thumbnail_url(episode.podcast.image),
                    "slug": episode.slug,
                    "podcast_slug": episode.podcast.slug,
                    "podcast_category": None,
                    "external_url": episode.url,
                }
            )

        context.update(
            {
                "seo": {
                    "title": f"Najnovejše epizode v kategoriji {category_i18n} | podcasti.si",
                    "description": (
                        f'Najnovejše podcast epizode v kategoriji "{category_i18n}". Najdi epizodo '
                        "ali podcast, ki te zanima!"
                    ),
                },
                "header": {
                    "url": "https://podcasti.si",
                    "title": "Slovenski Podcasti",
                    "subtitle": "Seznam vseh slovenskih podcastov",
                },
                "title": f'Najnovejše v kategoriji "{category_i18n}"',
                "latest_episodes": episodes,
                "paginator": latest_episodes,
                "filter_by": filter_by,
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
    queryset = (
        Episode.objects.prefetch_related("podcast")
        .exclude(published_datetime=None)
        .order_by("-published_datetime", "-created_datetime")
    )
    serializer_class = serializers.FeedSerializer


router = routers.DefaultRouter()
router.register(r"episodes", ApiEpisodes, "episode")
router.register(r"podcasts", ApiPodcasts, "podcast")
router.register(r"feed", ApiFeed, "feed")
