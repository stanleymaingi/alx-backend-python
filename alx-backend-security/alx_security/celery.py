# alx_security/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_security.settings")

app = Celery("alx_security")
# read config from Django settings (CELERY_* settings namespace)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# periodic schedule: run anomaly detection hourly
app.conf.beat_schedule = {
    "ip_tracking.detect-anomalies-hourly": {
        "task": "ip_tracking.tasks.detect_anomalies",
        "schedule": 3600.0,  # every hour
    },
}
