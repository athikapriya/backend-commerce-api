from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo users"

    def handle(self, *args, **options):
        
        users = [
            ("Customer1", "customer1@test.com"),
            ("Customer2", "customer2@test.com"),
            ("Customer3", "customer3@test.com"),
            ("Customer4", 'customer4@test.com'),
            ("Customer5", "customer5@test.com"),
        ]

        for username, email in users:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f"{username} already exists.")
                )
                continue

            User.objects.create_user(
                username=username,
                email=email,
                password="test123"
            )

            self.stdout.write(
                self.style.SUCCESS(f"{username} created successfully.")
            )