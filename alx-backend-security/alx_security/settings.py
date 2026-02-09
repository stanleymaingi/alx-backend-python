# alx_security/settings.py (snippets)
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET", "dev-secret-for-local")
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "django_ip_geolocation",  # django-ip-geolocation
    "ratelimit",              # django-ratelimit
    # "django_celery_beat",   # optional if you want DB-managed beat

    # local apps
    "ip_tracking.apps.IpTrackingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    # IP Geolocation middleware (adds request.geolocation if enabled)
    "django_ip_geolocation.middleware.IpGeolocationMiddleware",

    # Our custom middleware - runs after geolocation middleware so request.geolocation is available
    "ip_tracking.middleware.IPLoggingMiddleware",
]

ROOT_URLCONF = "alx_security.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Redis-backed cache (used both for rate-limit storage and caching geolocation)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Celery config
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"  # if using django-celery-beat
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

# django-ip-geolocation settings (example)
IP_GEOLOCATION_SETTINGS = {
    "BACKEND": "django_ip_geolocation.backends.IPGeolocationAPI",
    "BACKEND_API_KEY": os.getenv("IPGEO_API_KEY", ""),  # optional; uses free backend by default
    "ENABLE_REQUEST_HOOK": True,
    "ENABLE_RESPONSE_HOOK": False,
}

# Basic logging so that middleware logs go somewhere
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# Timezone
USE_TZ = True
TIME_ZONE = "UTC"

# Retention period for request logs (optional)
IP_TRACKING_RETENTION_DAYS = int(os.getenv("IP_TRACKING_RETENTION_DAYS", "30"))
