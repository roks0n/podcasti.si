import pytest
from django.urls import reverse

from tests.podcasts.factory import EpisodeFactory, PodcastFactory


def test_health_200(client):
    response = client.get(reverse("health"))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_get_episode_200(client):
    episode = EpisodeFactory()
    url_kwargs = {"podcast_slug": episode.podcast.slug, "episode_slug": episode.slug}
    response = client.get(reverse("episode", kwargs=url_kwargs))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_get_podcast_200(client):
    podcast = PodcastFactory()
    url_kwargs = {"podcast_slug": podcast.slug}
    response = client.get(reverse("podcast", kwargs=url_kwargs))
    assert response.status_code == 200
