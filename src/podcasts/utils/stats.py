# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import F

from podcasts.models import Stats


@transaction.atomic
def track_view(episode):
    try:
        stats = Stats.objects.select_for_update().get(episode=episode)
        stats.views = F('views') + 1
        stats.save()
    except Stats.DoesNotExist:
        Stats.objects.create(episode=episode)
