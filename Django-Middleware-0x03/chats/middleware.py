from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
import logging
import os

# ---------------------------
# Request Logging Middleware
# ---------------------------

log_file_path = os.path.join(os.path.dirname(__file__), 'requests.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    """
    Logs each user request with timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response

# ---------------------------
# Restrict Access By Time Middleware
# ---------------------------

class RestrictAccessByTimeMiddleware:
    """
    Denies access to the chat outside 6 PM to 9 PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chat/'):
            current_hour = datetime.now().hour
            if current_hour < 18 or current_hour >= 21:
                return HttpResponseForbidden(
                    "Chat access is only allowed between 6 PM and 9 PM."
                )
        response = self.get_response(request)
        return response

# ---------------------------
# Offensive Language / Rate Limit Middleware
# ---------------------------

MESSAGE_LIMIT = 5
TIME_WINDOW = timedelta(minutes=1)
ip_message_log = {}  # { ip_address: [datetime1, datetime2, ...] }

class OffensiveLanguageMiddleware:
    """
    Limits number of chat messages per IP per time window.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = datetime.now()
            timestamps = ip_message_log.get(ip, [])
            # Remove timestamps outside the time window
            timestamps = [t for t in timestamps if now - t < TIME_WINDOW]

            if len(timestamps) >= MESSAGE_LIMIT:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again later."},
                    status=429
                )

            timestamps.append(now)
            ip_message_log[ip] = timestamps

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# ---------------------------
# Role Permission Middleware
# ---------------------------

class RolePermissionMiddleware:
    """
    Only allows users with roles 'admin' or 'moderator' to access protected paths.
    """
    PROTECTED_PATHS = [
        '/chat/admin/',
        '/chat/manage/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.PROTECTED_PATHS):
            user = getattr(request, 'user', None)
            if not (user and user.is_authenticated and getattr(user, 'role', None) in ['admin', 'moderator']):
                return HttpResponseForbidden(
                    "You do not have permission to access this resource."
                )
        response = self.get_response(request)
        return response
