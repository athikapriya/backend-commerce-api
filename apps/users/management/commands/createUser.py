from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create a default Admin User"

    def handle(self, *args, options):
        username = "admin"
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists.')
            )

            return 
        
        User.objects.create_superuser(username=username, password="test123")
        self.stdout.write(
            self.style.SUCCESS(f'User {username} created successfully.')
        )