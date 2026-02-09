# ip_tracking/admin.py
from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "timestamp", "path", "country", "city")
    list_filter = ("country",)
    search_fields = ("ip_address", "path")

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "reason", "created_at")
    search_fields = ("ip_address",)

@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "reason", "flagged_at", "handled")
    list_filter = ("handled",)
