from django.core.management.base import BaseCommand
import random
from django.contrib.auth import get_user_model
from decimal import Decimal


from apps.products.models import Product
from apps.orders.models import Order, OrderItem


User = get_user_model()

class Command(BaseCommand):
    help = "Seed Orders"

    def handle(self, *args, **kwargs):

        users = User.objects.filter(is_superuser=False)

        if not users.exists():
            self.stdout.write(
                self.style.WARNING("User doesn't exist.")
            )
            return
        
        products = list(Product.objects.all())

        if not products:
            self.stdout.write(
                self.style.WARNING("No products found.")
            )
            return
        
        for user in users:
            order = Order.objects.create(
                user = user,
                total_price=Decimal("0.00")
            )

            selected_products = random.sample(
                products, 
                random.randint(2, 5)
            )

            total = 0

            for product in selected_products:
                quantity = random.randint(1, 3)

                OrderItem.objects.create(
                    order = order,
                    product = product,
                    quantity = quantity,
                    unit_price = product.price
                )

                total += product.price * quantity

            order.total_price = total
            order.save()

        self.stdout.write(
            self.style.SUCCESS("Orders seeded successfully.")
        )