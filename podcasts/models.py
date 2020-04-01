import uuid

from django.db import models
from django.utils.text import slugify


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    website = models.URLField(max_length=256, blank=True, null=True)
    authors = models.CharField(max_length=256, blank=True, null=True)
    feed_url = models.URLField(max_length=256)
    last_sync = models.DateTimeField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False)
    is_radio = models.NullBooleanField(default=False, db_index=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True, db_index=True
    )
    meta_description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f"{self.name} by {self.authors}"

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
    slug = models.SlugField(max_length=256, db_index=True)
    description = models.TextField()
    published_datetime = models.DateTimeField(null=True, blank=True, db_index=True)
    audio = models.URLField(max_length=256, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug", "podcast"]),
        ]

    def __str__(self):
        return f'{self.title} from "{self.podcast.name}"'

    def __repr__(self):
        return f'<Episode "{self.title}" from "{self.podcast.name}">'

    def save(self, *args, **kwargs):
        if not self.pk or not self.slug:
            slug = slugify(self.title)
            proposed_slug = slug if slug else str(uuid.uuid4())
            if not self.is_unique_slug(proposed_slug):
                proposed_slug = f"{proposed_slug}-{self.published_datetime.strftime('%Y-%m-%d')}"
            self.slug = proposed_slug
        super().save(*args, **kwargs)

    def is_unique_slug(self, slug):
        return not Episode.objects.filter(slug=slug).exists()


class Stats(models.Model):
    day = models.DateField(auto_now_add=True, db_index=True)
    views = models.IntegerField(default=1, db_index=True)
    episode_id = models.IntegerField(blank=True, null=True)
    podcast_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, db_index=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["day", "type", "views"]),
        ]

    def __str__(self):
        return f'{self.type} on "{self.day}"'

    def __repr__(self):
        return f'<Stats "{self.type}" on "{self.day}">'


class Category(models.Model):
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f'<Category "{self.name}">'
