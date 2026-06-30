from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.categories.models import Category


class Command(BaseCommand):
    help = "seed default categories"

    def handle(self, *args, **kwargs):
        categories = {

            "Food": [
                "Milk & Dairy",
                "Fruits & Vegetable",
                "Fish & Meat",
                "Snacks",
                "Beverages"
            ],

            "Electronics": [
                "Mobile Phones",
                "Laptops",
                "Accessories"
            ],

            "Fashion": [
                "Men",
                "Women"
            ]
        }

        for parent_name, children in categories.items():
            parent, _ = Category.objects.get_or_create(
                name = parent_name,
                defaults = {
                    "slug" : slugify(parent_name)
                }
            )

            for child_name in children:
                Category.objects.get_or_create(
                    name=child_name,
                    defaults={
                        "slug": slugify(child_name),
                        "parent": parent,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Categories seeded successfully.")
        )