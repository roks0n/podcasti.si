from podcasts import models

from rest_framework import serializers


class EpisodeSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(
        view_name="episode-detail", lookup_field="slug", read_only=True
    )

    class Meta:
        model = models.Episode
        fields = "__all__"
        exclude = ()


class PodcastSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(
        view_name="podcast-detail", lookup_field="slug", read_only=True
    )

    class Meta:
        model = models.Podcast
        fields = "__all__"
        exclude = ()


class FeedSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(
        view_name="feed-detail", lookup_field="slug", read_only=True
    )
    podcast = PodcastSerializer()

    class Meta:
        model = models.Episode
        fields = "__all__"
        exclude = ()
