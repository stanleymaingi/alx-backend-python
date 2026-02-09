# ip_tracking/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseTooManyRequests
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from ratelimit.core import is_ratelimited

SENSITIVE_PATHS = ["/admin", "/login"]

@csrf_exempt
def login_view(request):
    """
    A minimal login view demonstrating dynamic rate limiting:
    - authenticated users: 10 requests / minute
    - anonymous users: 5 requests / minute
    """
    # determine rate based on auth status
    if request.user.is_authenticated:
        rate = "10/m"
    else:
        rate = "5/m"

    # Use is_ratelimited with increment=True to count this request
    if is_ratelimited(request, rate=rate, key="ip", method="POST", increment=True):
        # return 429 Too Many Requests
        return HttpResponseTooManyRequests("Too many login attempts. Try again later.")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"ok": True})
        else:
            return JsonResponse({"ok": False, "detail": "Invalid credentials"}, status=401)

    # GET => render a simple form
    return HttpResponse(
        '<form method="post">'
        'Username: <input name="username"/><br>'
        'Password: <input type="password" name="password"/><br>'
        '<button type="submit">Login</button>'
        '</form>'
    )
