# ip_tracking/tests.py
from django.test import TestCase, Client
from django.urls import reverse

class IPTrackingSmokeTests(TestCase):
    def test_login_rate_limit_page(self):
        c = Client()
        resp = c.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
