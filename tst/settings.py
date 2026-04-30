# -*- coding: utf-8 -*-
"""Django settings for tests / type-checking."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test"
DEBUG = True
USE_TZ = True
TIME_ZONE = "UTC"

INSTALLED_APPS: list[str] = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "swing.error.apps.SwingErrorConfig",
]

MIDDLEWARE: list[str] = []

ROOT_URLCONF = "tst.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/swing_test_media"

# Common third-party / app-specific settings used by source code.
# Defined here so mypy_django_plugin sees them and doesn't raise
# "Settings object has no attribute X" for runtime-only config.
REDIS_HOST = "localhost"
REDIS_PORT = 6379
ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = 9200
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
SITEMAP_URL = "http://example.com/sitemap.xml"
BAIDU_API_TOKEN = "test-token"

# swing-cookie consent settings
COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 31536000
COOKIE_CONSENT_DOMAIN: str | None = None
COOKIE_CONSENT_SECURE = False
COOKIE_CONSENT_HTTPONLY = True
COOKIE_CONSENT_SAMESITE = "Lax"
COOKIE_CONSENT_DECLINE = "declined"
COOKIE_CONSENT_OPT_OUT = False
COOKIE_CONSENT_LOG_ENABLED = False
COOKIE_CONSENT_ENABLED = True
COOKIE_CONSENT_CACHE_BACKEND = "default"
