# ip_tracking/models.py
from django.db import models

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.ip_address

class RequestLog(models.Model):
    # We store an anonymized IP string for privacy
    ip_address = models.CharField(max_length=64, db_index=True)
    raw_ip = models.GenericIPAddressField(null=True, blank=True)  # optional, if you want to keep raw (be careful)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=10, default="GET")
    user_agent = models.CharField(max_length=512, blank=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    # optional: store additional JSON data (Geo coordinates etc.)
    extra = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.ip_address} {self.timestamp} {self.path}"

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(db_index=True)
    reason = models.CharField(max_length=400)
    flagged_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
