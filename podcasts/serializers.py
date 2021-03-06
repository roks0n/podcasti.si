from rest_framework import serializers

from podcasts import models


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
        exclude = ("meta_description",)


class FeedSerializer(serializers.ModelSerializer):
    _url = serializers.HyperlinkedIdentityField(
        view_name="feed-detail", lookup_field="slug", read_only=True
    )
    podcast = PodcastSerializer()

    class Meta:
        model = models.Episode
        fields = "__all__"
        exclude = ()
