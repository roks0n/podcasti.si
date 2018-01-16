# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from podcasts.models import Episode
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
        paginator = Paginator(latest_episodes, 25)
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
                'title': '',
                'description': '',
            },
            'header': {
                'url': 'example.com',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
            'latest_episodes': episodes,
            'paginator': latest_episodes
        })
        return context


class EpisodeView(TemplateView):
    template_name = 'episode.html'

    def get_context_data(self, podcast_slug, episode_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        episode = get_object_or_404(Episode, slug=episode_slug)
        context.update({
            'seo': {
                'title': '',
                'description': '',
            },
            'header': {
                'url': 'example.com',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
            'episode': episode
        })
        return context
