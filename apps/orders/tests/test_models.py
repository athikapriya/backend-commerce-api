import pytest
from decimal import Decimal

from apps.orders.models import OrderItem


# =============== Start Test for Item subtotal section ===============
@pytest.mark.django_db
def test_order_item_calculates_subtotal(order, product):
    item = OrderItem.objects.create(
        order=order,
        product=product,
        unit_price=Decimal("25.00"),
        quantity=3,
    )

    assert item.item_subtotal == Decimal("75.00")
# =============== End Test for Item subtotal seciton ===============


# =============== Start Test for zero/null unit price section ===============
@pytest.mark.django_db
def test_order_item_subtotal_is_zero_when_unit_price_is_zero(order, product):
    item = OrderItem.objects.create(
        order=order,
        product=product,
        unit_price=Decimal("0.00"),
        quantity=3,
    )

    assert item.item_subtotal == Decimal("0.00")
# =============== End Test for zero/null unit price seciton ===============


# =============== Start Test string representation section ===============
@pytest.mark.django_db
def test_order_item_string_representation(order, product):
    item = OrderItem.objects.create(
        order=order,
        product=product,
        unit_price=product.price,
        quantity=2,
    )

    assert str(item) == f"2 x {product.name}"
# =============== End Test string representation seciton ===============


# =============== Start Test Order string representation section ===============
@pytest.mark.django_db
def test_order_string_representation(order):
    assert str(order) == f"Order {order.order_id} by {order.user.username}"
# =============== End Test Order string representation seciton ===============