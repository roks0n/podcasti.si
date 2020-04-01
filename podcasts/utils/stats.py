from datetime import datetime

from django.db import transaction
from django.db.models import F
from podcasts.models import Stats


@transaction.atomic
def track_episode(episode):
    today = datetime.now()
    try:
        stats = Stats.objects.select_for_update().get(
            type="episode", episode_id=episode.pk, day=today,
        )
        stats.views = F("views") + 1
        stats.save()
    except Stats.DoesNotExist:
        data = {
            "type": "episode",
            "episode_id": episode.pk,
            "day": today,
        }
        Stats.objects.create(**data)


@transaction.atomic
def track_podcast(podcast):
    today = datetime.now()
    try:
        stats = Stats.objects.select_for_update().get(
            type="podcast", podcast_id=podcast.pk, day=today,
        )
        stats.views = F("views") + 1
        stats.save()
    except Stats.DoesNotExist:
        data = {
            "type": "podcast",
            "podcast_id": podcast.pk,
            "day": today,
        }
        Stats.objects.create(**data)
