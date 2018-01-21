# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from podcasts.models import Episode, Podcast
from podcasts.utils.stats import track_episode, track_podcast
from podcasts.utils.time import pretty_date


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        episodes = []

        page = self.request.GET.get('page')

        latest_episodes = Episode.objects.order_by('-published_datetime')
        paginator = Paginator(latest_episodes, 30)
        latest_episodes = paginator.get_page(page)

        for episode in latest_episodes:
            episodes.append({
                'title': episode.title,
                'podcast_name': episode.podcast.name,
                'published': pretty_date(episode.published_datetime),
                'image': episode.podcast.image.url,
                'slug': episode.slug,
                'podcast_slug': episode.podcast.slug,
                'external_url': episode.url,
            })

        context.update({
            'seo': {
                'title': 'Slovenski Podcasti - Največji seznam slovenskih podcastov',
                'description': (
                    'Največji seznam slovenskih podcastov. Odkrij, spremljaj in poslušaj '
                    'slovenske podcaste.'
                ),
            },
            'header': {
                'url': 'https://podcasti.si',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
            'latest_episodes': episodes,
            'paginator': latest_episodes,
            'featured_podcasts': Podcast.objects.order_by('?')[:8]
        })
        return context


class EpisodeView(TemplateView):
    template_name = 'episode.html'

    def get_context_data(self, podcast_slug, episode_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = get_object_or_404(Podcast, slug=podcast_slug)
        episode = get_object_or_404(Episode, slug=episode_slug, podcast=podcast)

        track_episode(episode)
        track_podcast(podcast)

        context.update({
            'seo': {
                'title': '{} | podcasti.si'.format(episode.title),
                'description': episode.description,
            },
            'header': {
                'url': 'https://podcasti.si',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
            'episode': episode
        })
        return context


class PodcastView(TemplateView):
    template_name = 'podcast.html'

    def get_context_data(self, podcast_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = get_object_or_404(Podcast, slug=podcast_slug)

        track_podcast(podcast)

        page = self.request.GET.get('page')

        latest_episodes = podcast.episode_set.order_by('-published_datetime')
        paginator = Paginator(latest_episodes, 30)
        latest_episodes = paginator.get_page(page)

        episodes = []
        for episode in latest_episodes:
            episodes.append({
                'title': episode.title,
                'podcast_name': episode.podcast.name,
                'published': pretty_date(episode.published_datetime),
                'slug': episode.slug,
                'podcast_slug': episode.podcast.slug,
                'external_url': episode.url,
            })

        context.update({
            'seo': {
                'title': '{} Podcast | podcasti.si'.format(podcast.name),
                'description': podcast.description
            },
            'header': {
                'url': 'https://podcasti.si',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
            'podcast': podcast,
            'episodes': episodes,
            'paginator': latest_episodes
        })
        return context
