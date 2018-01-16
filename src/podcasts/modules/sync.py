# -*- coding: utf-8 -*-
from podcasts.models import Episode
from podcasts.modules.parsers.base import DefaultPodcastParser


def sync_podcast(podcast):
    parser = DefaultPodcastParser(podcast.feed_url)
    episodes = parser.parse()

    for episode in episodes:
        if not Episode.objects.filter(title=episode['title'], podcast=podcast).exists():
            episode.update({'podcast': podcast})
            Episode.objects.create(**episode)
