import pytest
from rest_framework import serializers

from apps.orders.serializers import OrderCreateSerializer


# =============== Start Test Duplicate Products section ===============
@pytest.mark.django_db
def test_order_serializer_rejects_duplicate_products(product):
    data = {
        "items": [
            {
                "product": product.id,
                "quantity": 1,
            },
            {
                "product": product.id,
                "quantity": 2,
            },
        ]
    }

    serializer = OrderCreateSerializer(data=data)
    assert serializer.is_valid() is False
    assert "items" in serializer.errors
# =============== End Test Duplicate Products seciton ===============


# =============== Start Test empty items are rejected section ===============
@pytest.mark.django_db
def test_order_serializer_rejects_empty_items():
    serializer = OrderCreateSerializer(
        data={
            "items": []
        }
    )

    assert serializer.is_valid() is False
    assert "items" in serializer.errors
# =============== End Test empty items are rejected seciton ===============


# =============== Start Test insufficient stock section ===============
@pytest.mark.django_db
def test_order_serializer_rejects_insufficient_stock(user, product):
    serializer = OrderCreateSerializer(
        data={
            "items": [
                {
                    "product": product.id,
                    "quantity": product.stock + 1,
                }
            ]
        }
    )

    assert serializer.is_valid()
    with pytest.raises(serializers.ValidationError):
        serializer.save(user=user)
# =============== End Test insufficient stock seciton ===============