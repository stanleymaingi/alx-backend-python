# ip_tracking/tasks.py
from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task(bind=True)
def detect_anomalies(self):
    """
    Flags IPs as suspicious if:
      - More than 100 requests in the last hour OR
      - Any access to sensitive paths (e.g., /admin, /login) in the last hour
    Adds entries to SuspiciousIP model with reason.
    """
    now = timezone.now()
    since = now - timedelta(hours=1)

    # 1) high request count detection
    hits = (
        RequestLog.objects.filter(timestamp__gte=since)
        .values("raw_ip")
        .annotate(count=Count("id"))
        .filter(count__gt=100)
    )

    flagged = []
    for h in hits:
        ip = h["raw_ip"]
        count = h["count"]
        reason = f"High request rate: {count} reqs in last hour"
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason=reason)
        flagged.append((ip, reason))

    # 2) sensitive path access detection (flag any IP that accessed those paths)
    sensitive_paths = ["/admin", "/login"]
    sips = (
        RequestLog.objects.filter(timestamp__gte=since, path__in=sensitive_paths)
        .values("raw_ip")
        .distinct()
    )
    for row in sips:
        ip = row["raw_ip"]
        reason = f"Accessed sensitive path in last hour: paths={sensitive_paths}"
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason=reason)
        flagged.append((ip, reason))

    return {"flagged": flagged}
