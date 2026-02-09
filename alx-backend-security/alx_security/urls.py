# alx_security/urls.py
from django.contrib import admin
from django.urls import path, include
from ip_tracking.views import login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    # add other app urls...
]
