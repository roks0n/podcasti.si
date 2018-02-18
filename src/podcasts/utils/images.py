from sorl.thumbnail import get_thumbnail


def get_thumbnail_url(image, size):
    thumbnail = get_thumbnail(image, size, crop='center', quality=100, format="PNG")
    image_url = thumbnail.url.replace(
        'https://s3.amazonaws.com',
        'https://s3.eu-west-3.amazonaws.com'
    )
    return image_url
