"""
Django settings for podcasts project.
"""

import logging

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

root = environ.Path(__file__) - 2
env = environ.Env()

DEBUG = env.bool("DEBUG", default=False)

# Do not auto-append trailing slashes to URLs. Auto-appending slashes caused
# confusing bugs if client code is not written with the correct urls, because
# the redirection does not play nicely with PUT/POST data. Better to just raise
# a 404, which makes it obvious the need to fix the client code.
APPEND_SLASH = False

DATABASES = {
    "default": env.db_url("DATABASE_URL", default="postgres://postgres:postgres@db:5432/postgres")
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
SECRET_KEY = env.str("SECRET_KEY", default="please-dont-use-me-in-production")

# Application definition
if DEBUG:
    INSTALLED_APPS = ("whitenoise.runserver_nostatic",)
else:
    INSTALLED_APPS = ()

INSTALLED_APPS += (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "rest_framework",
    "storages",
    "podcasts",
)


SITE_ID = 1
INSTALLED_APPS += ("django.contrib.sites", "django.contrib.sitemaps")

REST_FRAMEWORK = {
    # Use only JSON by default
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": ("rest_framework.renderers.JSONRenderer",),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "podcasts.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = root("static")

STATICFILES_DIRS = (root("static-source/"),)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    WHITENOISE_AUTOREFRESH = True

# S3 settings for uploaded files
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_REGION_NAME = env.str("AWS_REGION", default=None)
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default=None)
AWS_QUERYSTRING_AUTH = False
MEDIA_URL = env.str("MEDIA_URL", default="/media/")
if DEBUG:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = root("../media/")
else:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    MEDIA_ROOT = ""
PAGE_SIZE = 30
REST_FRAMEWORK = {
    "PAGE_SIZE": PAGE_SIZE,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}
    },
    "loggers": {
        "django": {"propagate": True, "level": "INFO"},
        "django.security.DisallowedHost": {"propagate": False, "handlers": []},
        "podcasts": {"propagate": True, "level": "INFO"},
        "": {"handlers": ["console"], "level": "ERROR"},
    },
}

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN", default=""), integrations=[sentry_logging, DjangoIntegration()]
)
