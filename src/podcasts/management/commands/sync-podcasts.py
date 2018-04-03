import sys

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from podcasts.models import Podcast
from podcasts.modules.sync import sync_podcast


class Command(BaseCommand):

    def handle(self, *args, **options):
        sync_podcasts = Podcast.objects.filter(
            Q(last_sync=None) | Q(last_sync__lte=timezone.now() - timedelta(hours=1))
        )
        for podcast in sync_podcasts:
            sys.stdout.write('Syncing podcast {}\n'.format(podcast.name))
            sync_podcast(podcast)
            podcast.last_sync = timezone.now()
            podcast.save()
