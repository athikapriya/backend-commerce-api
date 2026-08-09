import pytest
from rest_framework.test import APIClient

from factories import UserFactory, AdminFactory, CategoryFactory, ProductFactory
from apps.orders.models import Order


# ===== start api_client =====
@pytest.fixture
def api_client():
    return APIClient()
# ===== End api_client =====


# ===== start user =====
@pytest.fixture
def user(db):
    return UserFactory()
# ===== End user =====


# ===== start admin =====
@pytest.fixture
def admin(db):
    return AdminFactory()
# ===== End admin =====


# ===== start category =====
@pytest.fixture
def category(db):
    return CategoryFactory()
# ===== End category =====


# ===== start product =====
@pytest.fixture
def product(db):
    return ProductFactory()
# ===== End product =====


# ===== start order =====
@pytest.fixture
def order(db, user):
    return Order.objects.create(
        user=user,
        total_price=100,
        order_status=Order.StatusChoices.PENDING,
        payment_status=Order.PaymentStatus.PENDING,
    )
# ===== End order =====