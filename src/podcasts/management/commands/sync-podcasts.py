# -*- coding: utf-8 -*-
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from podcasts.models import Podcast
from podcasts.modules.sync import sync_podcast


class Command(BaseCommand):

    def handle(self, *args, **options):
        sync_podcasts = Podcast.objects.filter(
            Q(last_sync=None) | Q(last_sync__gte=timezone.now() - timedelta(hours=1))
        )
        for podcast in sync_podcasts:
            sync_podcast(podcast)
            podcast.last_sync = timezone.now()
            podcast.save()