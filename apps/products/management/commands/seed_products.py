from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal

from apps.categories.models import Category
from apps.products.models import Product

class Command(BaseCommand):
    help = "Seed Products"

    def handle(self, *args, **kwargs):
        products = {

            "Milk & Dairy" : [
                ("Milk", Decimal("90.00"), 100),
                ("Cheese", Decimal("350.00"), 30),
                ("Butter", Decimal("240.00"), 40),
                ("Yogurt", Decimal("80.00"), 70),
            ],

            "Fruits & Vegetable": [
                ("Tomato", Decimal("45.00"), 120),
                ("Potato", Decimal("35.00"), 200),
                ("Carrot", Decimal("60.00"), 90),
                ("Cabbage", Decimal("70.00"), 45),
                ("Apple", Decimal("250.00"), 50),
                ("Banana", Decimal("80.00"), 100),
                ("Orange", Decimal("180.00"), 60),
            ],

            "Fish & Meat": [
                ("Beef", Decimal("850.00"), 30),
                ("Chicken", Decimal("280.00"), 80),
                ("Hilsa Fish", Decimal("1400.00"), 15),
                ("Rohu Fish", Decimal("450.00"), 40),
                ("Mutton", Decimal("1100.00"), 20),
            ],

            "Snacks": [
                ("Potato Chips", Decimal("40.00"), 120),
                ("Biscuits", Decimal("30.00"), 150),
                ("Chocolate", Decimal("120.00"), 90),
                ("Popcorn", Decimal("80.00"), 70),
                ("Cookies", Decimal("150.00"), 60),
            ],

            "Beverages": [
                ("Orange Juice", Decimal("180.00"), 40),
                ("Apple Juice", Decimal("200.00"), 35),
                ("Mineral Water", Decimal("30.00"), 300),
                ("Coffee", Decimal("450.00"), 25),
                ("Green Tea", Decimal("300.00"), 40),
            ],

            "Mobile Phones": [
                ("iPhone 15", Decimal("120000.00"), 8),
                ("Samsung Galaxy S25", Decimal("95000.00"), 12),
                ("Google Pixel 9", Decimal("98000.00"), 7),
                ("Xiaomi 15", Decimal("65000.00"), 15),
            ],

            "Laptops": [
                ("MacBook Air M3", Decimal("175000.00"), 5),
                ("Dell XPS 13", Decimal("165000.00"), 6),
                ("Lenovo ThinkPad X1", Decimal("185000.00"), 4),
                ("ASUS Zenbook 14", Decimal("140000.00"), 8),
            ],

            "Accessories": [
                ("Wireless Mouse", Decimal("1800.00"), 50),
                ("Mechanical Keyboard", Decimal("6500.00"), 20),
                ("USB-C Charger", Decimal("2500.00"), 35),
                ("Bluetooth Earbuds", Decimal("5500.00"), 40),
                ("Laptop Backpack", Decimal("3200.00"), 25),
            ],

            "Men": [
                ("Men's T-Shirt", Decimal("850.00"), 100),
                ("Men's Jeans", Decimal("2200.00"), 60),
                ("Men's Polo Shirt", Decimal("1400.00"), 45),
                ("Men's Sneakers", Decimal("4500.00"), 30),
                ("Men's Hoodie", Decimal("2800.00"), 25),
            ],

            "Women": [
                ("Women's Kurti", Decimal("1800.00"), 50),
                ("Women's Jeans", Decimal("2400.00"), 40),
                ("Women's Handbag", Decimal("3500.00"), 20),
                ("Women's Sneakers", Decimal("4800.00"), 25),
                ("Women's Scarf", Decimal("600.00"), 70),
            ],

        }

        for category_name, items in products.items():
            try:
                category = Category.objects.get(name = category_name)

            except Category.DoesNotExist :
                self.stdout.write(
                    self.style.WARNING(f'{category_name} not found.')
                )
                continue
            
            for name, price, stock in items:
                Product.objects.get_or_create(
                    name = name,
                    defaults={
                        "category" : category,
                        "price" : price,
                        "stock" : stock,
                        "description" : f'{name} description'
                    }
                )
            
        self.stdout.write(
            self.style.SUCCESS("Products seeded successfully.")
        )