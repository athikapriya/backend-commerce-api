from django.db import models
from django.contrib.auth import get_user_model
import uuid
from decimal import Decimal

from apps.products.models import Product

User = get_user_model()


# =============== Start Order Model section ===============
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELED = "CANCELED", "Canceled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(Product, through="OrderItem", related_name="order_items")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'Order {self.order_id} by {self.user.username}'
# =============== End Order Model seciton ===============



# =============== Start OrderItem Model section ===============
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_subtotal(self):
        return (self.unit_price or Decimal("0.00")) * self.quantity
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", 'product'],
                name="unique_product_per_order"
            )
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
# =============== End OrderItem Model seciton ===============