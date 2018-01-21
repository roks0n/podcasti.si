# -*- coding: utf-8 -*-
from podcasts.models import Episode
from podcasts.modules.parsers.base import (
    BitniPogovoriParser, DefaultPodcastParser, FeedBurnerParser, FilmStartParser, SoundcloudParser,
    TorpedoParser, ZakulisjeParser
)


def sync_podcast(podcast):
    if podcast.slug == 'zakulisje':
        parser = ZakulisjeParser(podcast.feed_url)
    elif podcast.slug == 'filmstart':
        parser = FilmStartParser(podcast.feed_url)
    elif podcast.slug in ['torpedo', 'membranje', 'fotkast', 'the-tranzistorij']:
        parser = TorpedoParser(podcast.feed_url)
    elif podcast.slug in ['bitni-pogovori', 'na-potezi']:
        parser = BitniPogovoriParser(podcast.feed_url)
    elif podcast.slug == ['bimpogovori']:
        parser = FeedBurnerParser(podcast.feed_url)
    elif 'feeds.soundcloud.com' in podcast.feed_url:
        parser = SoundcloudParser(podcast.feed_url)
    else:
        parser = DefaultPodcastParser(podcast.feed_url)

    episodes = parser.parse()
    for episode in episodes:
        if not Episode.objects.filter(title=episode['title'], podcast=podcast).exists():
            episode.update({'podcast': podcast})
            Episode.objects.create(**episode)
