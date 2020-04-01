from datetime import datetime

import pytest

from podcasts.models import Episode


@pytest.mark.django_db()
def test_save_episode_and_dups():
    Episode.objects.create(
        **{
            "identifier": "unique",
            "title": "Bombastic",
            "description": "Supa Bombastic, Mr. Fantastic",
            "published_datetime": datetime.utcnow(),
        }
    )
    assert Episode.objects.get().slug == "bombastic"

    Episode.objects.create(
        **{
            "identifier": "unique",
            "title": "Bombastic",
            "description": "Supa Bombastic, Mr. Fantastic",
            "published_datetime": datetime.utcnow(),
        }
    )

    assert Episode.objects.count() == 2
    assert Episode.objects.last().slug == f"bombastic-{datetime.now().strftime('%Y-%m-%d')}"


@pytest.mark.django_db()
def test_save_episode_empty_slugify_result():
    Episode.objects.create(
        **{
            "identifier": "unique",
            "title": "✅✌️🚨",
            "description": "Supa Bombastic, Mr. Fantastic",
            "published_datetime": datetime.utcnow(),
        }
    )
    assert Episode.objects.get().slug
