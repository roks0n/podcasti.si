import sys

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from podcasts.models import Podcast
from podcasts.modules.sync import sync_podcast
from podcasts.utils.logger import get_log

log = get_log(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        sync_podcasts = Podcast.objects.filter(
            Q(last_sync=None) | Q(last_sync__lte=timezone.now() - timedelta(hours=1)),
            disabled=False
        )
        for podcast in sync_podcasts:
            sys.stdout.write('Syncing podcast {}\n'.format(podcast.name))
            try:
                sync_podcast(podcast)
            except Exception:
                log.exception('Error syncing podcast %s. Marking it as disabled.', podcast.name)
                podcast.disabled = True
            else:
                podcast.last_sync = timezone.now()
            podcast.save()
