from podcasts.models import Episode
from podcasts.modules.parsers.base import BasePodcastParser, DefaultPodcastParser


def get_parser(base_class, class_name):
    def all_parser_classes(cls):
        for subclass in cls.__subclasses__():
            yield from all_parser_classes(subclass)
            yield subclass

    return next(
        (
            cls
            for cls in all_parser_classes(base_class)
            if cls.__name__.lower() == class_name.lower()
        ),
        None,
    )


def sync_podcast(podcast):
    class_name = f'{podcast.slug.replace("-", "")}parser'
    parser_class = get_parser(BasePodcastParser, class_name)

    if parser_class:
        parser = parser_class(podcast.feed_url)
    else:
        parser = DefaultPodcastParser(podcast.feed_url)

    episodes = parser.parse()
    ident_name = parser.episode_identifier

    for episode in episodes:
        episodes_query = Episode.objects.filter(
            **{ident_name: episode[ident_name], "podcast": podcast}
        )

        if not episodes_query.exists():
            episode.update({"podcast": podcast})
            Episode.objects.create(**episode)
