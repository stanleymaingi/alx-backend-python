# ip_tracking/middleware.py
import logging
import ipaddress
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.conf import settings
from django.core.cache import cache

from ipware import get_client_ip
from .models import RequestLog, BlockedIP

logger = logging.getLogger(__name__)

def anonymize_ip(ip_str):
    """Anonymize IP: mask IPv4 to /24 and IPv6 to /64 for privacy."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except Exception:
        return ip_str
    if ip.version == 4:
        network = ipaddress.ip_network(f"{ip_str}/24", strict=False)
        return str(network.network_address)  # e.g., 192.168.1.0
    else:
        # IPv6 /64
        network = ipaddress.ip_network(f"{ip_str}/64", strict=False)
        return str(network.network_address)

class IPLoggingMiddleware:
    """
    Logs incoming requests (IP, timestamp, path). Blocks IPs present in BlockedIP.
    Uses django-ip-geolocation's request.geolocation if available.
    Caches geolocation lookups for 24 hours with key 'geo:{ip}'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        # If we couldn't get a client ip, we log as unknown
        if client_ip is None:
            client_ip = "0.0.0.0"

        # Check blacklist using cache-first approach
        blocked_cache_key = f"blocked_ip:{client_ip}"
        blocked = cache.get(blocked_cache_key)
        if blocked is None:
            blocked = BlockedIP.objects.filter(ip_address=client_ip).exists()
            cache.set(blocked_cache_key, blocked, timeout=60 * 5)  # short cache for admin changes
        if blocked:
            logger.warning("Blocked request from %s", client_ip)
            return HttpResponseForbidden("Forbidden: your IP is blocked.")

        # Get geolocation (cached)
        geo_cache_key = f"geo:{client_ip}"
        geo = cache.get(geo_cache_key)
        if geo is None:
            # try to use request.geolocation (populated by django-ip-geolocation middleware)
            geo = {}
            geoloc = getattr(request, "geolocation", None)
            if geoloc:
                # geoloc typically has .country and .city or ._country/_geo depending on backend
                try:
                    country = None
                    city = None
                    if hasattr(geoloc, "_country"):
                        country = geoloc._country.get("name")
                    elif getattr(geoloc, "country", None):
                        country = geoloc.country.get("name") if isinstance(geoloc.country, dict) else geoloc.country
                    city = getattr(geoloc, "_city", None) or getattr(geoloc, "city", None)
                    # allow geoloc._geo for lat/lon
                    latlon = getattr(geoloc, "_geo", None) or getattr(geoloc, "geo", None)
                    geo = {"country": country, "city": city, "geo": latlon}
                except Exception:
                    geo = {}
            # cache for 24 hours
            cache.set(geo_cache_key, geo, timeout=60 * 60 * 24)
        country = geo.get("country") if geo else None
        city = geo.get("city") if geo else None

        # Anonymize IP before storing
        anon_ip = anonymize_ip(client_ip)

        # User agent
        ua = request.META.get("HTTP_USER_AGENT", "")[:512]

        # Save request log (non-blocking: small DB write)
        try:
            RequestLog.objects.create(
                ip_address=anon_ip,
                raw_ip=client_ip,
                path=request.path[:512],
                method=request.method,
                user_agent=ua,
                country=country,
                city=city,
                extra=geo or None,
            )
        except Exception as e:
            logger.exception("Failed to write RequestLog: %s", e)

        # continue response
        response = self.get_response(request)
        return response
