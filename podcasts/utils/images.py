from django.conf import settings


def get_thumbnail_url(image):
    if not image:
        # TODO: change this with a proper default
        return "https://placehold.it/500x500?text=n/a"
    if settings.DEBUG:
        return "https://s3.eu-west-3.amazonaws.com/podcasti.si/{}".format(image)
    return image.url.replace("https://s3.amazonaws.com", "https://s3.eu-west-3.amazonaws.com")
