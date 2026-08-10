from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from drf_spectacular.utils import extend_schema_field

from .models import Order, OrderItem
from apps.products.models import Product


# =============== Start OrderItem serializer section ===============
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    item_subtotal = serializers.SerializerMethodField()

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_item_subtotal(self, obj):
        return obj.item_subtotal

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "unit_price",
            "quantity",
            "item_subtotal",
        )
# =============== End OrderItem serializer seciton ===============


# =============== Start OrderItemCreateSerializer section ===============
class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity"
        )
# =============== End OrderItemCreateSerializer seciton ===============


# =============== Start OrderCreateSerializer section ===============
class OrderCreateSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, allow_empty=False)

    def _calculate_total(self, order, items_data):
        total_price = Decimal("0.00")

        product_ids = [item["product"].id for item in items_data]

        locked_products = {
            p.id: p
            for p in Product.objects.select_for_update().filter(
                id__in=product_ids
            ).order_by("id")
        }

        for item in items_data:
            product = locked_products[item["product"].id]
            quantity = item["quantity"]

            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"{product.name} has only {product.stock} items left."
                )

        for item in items_data:
            product = locked_products[item["product"].id]
            quantity = item["quantity"]
            unit_price = product.price

            product.stock -= quantity
            product.save(update_fields=["stock"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
            )

            total_price += unit_price * quantity

        order.total_price = total_price
        order.save(update_fields=["total_price"])

    def validate_items(self, value):
        product_ids = [item["product"].id for item in value]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Duplicate products are not allowed."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items", [])

        order = Order.objects.create(**validated_data)

        self._calculate_total(order, items_data)

        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        if (
            items_data is not None
            and instance.order_status != Order.StatusChoices.PENDING
        ):
            raise serializers.ValidationError(
                "Only pending orders can be modified."
            )

        instance = super().update(instance, validated_data)

        if items_data is None:
            return instance

        old_items = list(instance.items.all())

        product_ids = [item.product_id for item in old_items]

        locked_products = {
            p.id: p
            for p in Product.objects.select_for_update()
            .filter(id__in=product_ids)
            .order_by("id")
        }

        for item in old_items:
            product = locked_products[item.product_id]
            product.stock += item.quantity
            product.save(update_fields=["stock"])

        instance.items.all().delete()

        self._calculate_total(instance, items_data)

        return instance

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")
        if request and not request.user.is_staff:
            fields["order_status"].read_only = True

        return fields

    class Meta:
        model = Order
        fields = (
            "order_id",
            "order_status",
            "items",
        )
# =============== End OrderCreateSerializer seciton ===============


# =============== Start Order Serializer section ===============
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    order_id = serializers.UUIDField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = (
            "user",
            "order_id",
            "order_status",
            "payment_status",
            "items",
            "created_at",
            "total_price",
        )
# =============== End Order Serializer seciton ===============