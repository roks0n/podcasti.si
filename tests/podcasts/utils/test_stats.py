from datetime import datetime

from freezegun import freeze_time
from podcasts.models import Stats
from podcasts.utils import stats
import pytest

from tests.podcasts.factory import EpisodeFactory, PodcastFactory


@pytest.mark.django_db()
def test_track_episode():
    episode1 = EpisodeFactory()
    episode2 = EpisodeFactory()

    with freeze_time("2020-04-01"):
        stats.track_episode(episode1)
        stats.track_episode(episode1)
        stats.track_episode(episode1)
        stats.track_episode(episode2)

    # validate results for 2020-04-01
    ep1_results = Stats.objects.filter(episode_id=episode1.id, day=datetime(2020, 4, 1))
    ep2_results = Stats.objects.filter(episode_id=episode2.id, day=datetime(2020, 4, 1))
    assert ep1_results.count() == 1
    assert ep1_results.get().views == 3
    assert ep2_results.count() == 1
    assert ep2_results.get().views == 1

    with freeze_time("2020-04-02"):
        stats.track_episode(episode1)
        stats.track_episode(episode1)
        stats.track_episode(episode2)
        stats.track_episode(episode2)

    # validate results for 2020-04-02
    ep1_results = Stats.objects.filter(episode_id=episode1.id, day=datetime(2020, 4, 2))
    ep2_results = Stats.objects.filter(episode_id=episode2.id, day=datetime(2020, 4, 2))
    assert ep1_results.count() == 1
    assert ep1_results.get().views == 2
    assert ep2_results.count() == 1
    assert ep2_results.get().views == 2


@pytest.mark.django_db()
def test_track_podcast():
    podcast1 = PodcastFactory()
    podcast2 = PodcastFactory()

    with freeze_time("2020-04-01"):
        stats.track_podcast(podcast1)
        stats.track_podcast(podcast1)
        stats.track_podcast(podcast1)
        stats.track_podcast(podcast2)

    # validate results for 2020-04-01
    p1_results = Stats.objects.filter(podcast_id=podcast1.id, day=datetime(2020, 4, 1))
    p2_results = Stats.objects.filter(podcast_id=podcast2.id, day=datetime(2020, 4, 1))
    assert p1_results.count() == 1
    assert p1_results.get().views == 3
    assert p2_results.count() == 1
    assert p2_results.get().views == 1

    with freeze_time("2020-04-02"):
        stats.track_podcast(podcast1)
        stats.track_podcast(podcast1)
        stats.track_podcast(podcast2)
        stats.track_podcast(podcast2)

    # validate results for 2020-04-02
    p1_results = Stats.objects.filter(podcast_id=podcast1.id, day=datetime(2020, 4, 2))
    p2_results = Stats.objects.filter(podcast_id=podcast2.id, day=datetime(2020, 4, 2))
    assert p1_results.count() == 1
    assert p1_results.get().views == 2
    assert p2_results.count() == 1
    assert p2_results.get().views == 2
