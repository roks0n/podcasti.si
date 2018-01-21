# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import F

from podcasts.models import Stats


@transaction.atomic
def track_episode(episode):
    try:
        stats = Stats.objects.select_for_update().get(
            payload__type='episode',
            payload__episode_id=episode.pk
        )
        stats.views = F('views') + 1
        stats.save()
    except Stats.DoesNotExist:
        payload = {
            'type': 'episode',
            'episode_id': episode.pk
        }
        Stats.objects.create(payload=payload)


@transaction.atomic
def track_podcast(podcast):
    try:
        stats = Stats.objects.select_for_update().get(
            payload__type='podcast',
            payload__podcast_id=podcast.pk
        )
        stats.views = F('views') + 1
        stats.save()
    except Stats.DoesNotExist:
        payload = {
            'type': 'podcast',
            'podcast_id': podcast.pk
        }
        Stats.objects.create(payload=payload)
