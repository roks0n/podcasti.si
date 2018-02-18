def get_thumbnail_url(image, size):
    image_url = image.url.replace(
        'https://s3.amazonaws.com',
        'https://s3.eu-west-3.amazonaws.com'
    )
    return image_url
