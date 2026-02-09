# ip_tracking/management/commands/block_ip.py
from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Add an IP to the BlockedIP table"

    def add_arguments(self, parser):
        parser.add_argument("ip", type=str, help="IP address to block")
        parser.add_argument("--reason", type=str, default="", help="Reason for blocking")

    def handle(self, *args, **options):
        ip = options["ip"]
        reason = options["reason"]
        obj, created = BlockedIP.objects.get_or_create(ip_address=ip, defaults={"reason":reason})
        if created:
            self.stdout.write(self.style.SUCCESS(f"Blocked IP {ip} (reason: {reason})"))
        else:
            self.stdout.write(self.style.WARNING(f"IP {ip} is already blocked"))
