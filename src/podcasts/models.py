from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    website = models.URLField(max_length=256, blank=True, null=True)
    authors = models.CharField(max_length=256, blank=True, null=True)
    feed_url = models.URLField(max_length=256)
    last_sync = models.DateTimeField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False)
    is_radio = models.NullBooleanField(default=False)

    def __str__(self):
        return f'{self.name} by {self.authors}'

    def __repr__(self):
        return f'<Podcast "{self.name}" by "{self.authors}">'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Episode(models.Model):
    identifier = models.CharField(max_length=256, null=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField()
    published_datetime = models.DateTimeField(null=True, blank=True)
    audio = models.URLField(max_length=256, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} from "{self.podcast.name}"'

    def __repr__(self):
        return f'<Episode "{self.title}" from "{self.podcast.name}">'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Stats(models.Model):
    day = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=1)
    payload = JSONField(default=dict)

    def __str__(self):
        return f'{self.payload["type"]} on "{self.day}"'

    def __repr__(self):
        return f'<Stats "{self.payload["type"]}" on "{self.day}">'
