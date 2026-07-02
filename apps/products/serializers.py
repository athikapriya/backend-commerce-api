from rest_framework import serializers

from .models import Product


# =============== Start ProductSerializer section ===============
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must me greater than 0")
        return value
# =============== End ProductSerializer seciton ===============
