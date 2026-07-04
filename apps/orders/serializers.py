from rest_framework import serializers

from .models import Order, OrderItem


# =============== Start OrderItem serializer section ===============
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    item_subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "unit_price",
            "quantity",
            "item_subtotal"
        )
# =============== End OrderItem serializer seciton ===============



# =============== Start Order Serializer section ===============
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Order
        fields = (
            'user',
            "status",
            "order_id",
            "created_at",
            "items",
            "total_price"
        )
# =============== End Order Serializer seciton ===============