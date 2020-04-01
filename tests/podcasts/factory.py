import factory
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()


class PodcastFactory(DjangoModelFactory):
    class Meta:
        model = "podcasts.Podcast"

    name = factory.Faker("bs")
    description = factory.Faker("text")
    feed_url = f"{fake.url()}feed.xml"
    website = fake.url()
    authors = factory.Faker("name")
    is_radio = factory.Iterator([True, False])


class EpisodeFactory(DjangoModelFactory):
    class Meta:
        model = "podcasts.Episode"

    identifier = factory.Faker("uuid4")
    podcast = factory.SubFactory(PodcastFactory)
    title = factory.Faker("bs")
    description = factory.Faker("text")
    audio = factory.Sequence(lambda n: f"{fake.url()}files/{n}_audio.mp3")
    url = fake.url()
