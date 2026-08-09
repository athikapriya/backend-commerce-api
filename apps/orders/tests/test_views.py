import pytest
from rest_framework import status

from apps.orders.models import Order
from factories import UserFactory


# =============== Start Customer can create an order test section ===============
@pytest.mark.django_db
def test_customer_can_create_order(api_client, user, product):
    api_client.force_authenticate(user=user)
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 2,
            }
        ]
    }

    response = api_client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    order = Order.objects.get(user=user)
    assert order.total_price == product.price * 2
# =============== End Customer can create an order test seciton ===============


# =============== Start Stock is deducted test section ===============
@pytest.mark.django_db
def test_creating_order_reduces_product_stock(api_client, user, product):
    initial_stock = product.stock
    api_client.force_authenticate(user=user)
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 3,
            }
        ]
    }

    response = api_client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    product.refresh_from_db()
    assert product.stock == initial_stock - 3
# =============== End Stock is deducted test seciton ===============


# =============== Start Prevents overselling test section ===============
@pytest.mark.django_db
def test_cannot_create_order_when_stock_is_insufficient(api_client, user, product):
    initial_stock = product.stock
    api_client.force_authenticate(user=user)
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": initial_stock + 1,
            }
        ]
    }

    response = api_client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    product.refresh_from_db()
    assert product.stock == initial_stock
# =============== End Prevents overselling test seciton ===============


# =============== Start Prevents duplicate order items test section ===============
@pytest.mark.django_db
def test_cannot_create_order_with_duplicate_products(api_client, user, product):
    api_client.force_authenticate(user=user)
    payload = {
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

    response = api_client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
# =============== End Prevents duplicate order items test seciton ===============


# =============== Start Customer can access their order test section ===============
@pytest.mark.django_db
def test_customer_can_retrieve_own_order(api_client, user, order):
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/api/orders/{order.order_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["order_id"] == str(order.order_id)
# =============== End Customer can access their order test seciton ===============


# =============== Start Prevents accessing another user's order test section ===============
@pytest.mark.django_db
def test_customer_cannot_retrieve_another_users_order(api_client, user, order):
    another_user = UserFactory()
    api_client.force_authenticate(user=another_user)

    response = api_client.get(f"/api/orders/{order.order_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
# =============== End Prevents accessing another user's order test seciton ===============


# =============== Start customer can modify a pending order test section ===============
@pytest.mark.django_db
def test_customer_can_update_pending_order(api_client, user, order, product):
    api_client.force_authenticate(user=user)
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 3,
            }
        ]
    }

    response = api_client.put(f"/api/orders/{order.order_id}/", payload, format="json")
    assert response.status_code == status.HTTP_200_OK

    order.refresh_from_db()
    assert order.total_price == product.price * 3
# =============== End customer can modify a pending order test seciton ===============


# =============== Start customer cannot modify confirmed order test section ===============
@pytest.mark.django_db
def test_customer_cannot_update_confirmed_order(api_client, user, order, product):
    order.order_status = Order.StatusChoices.CONFIRMED
    order.save()

    api_client.force_authenticate(user=user)
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 2,
            }
        ]
    }

    response = api_client.put(f"/api/orders/{order.order_id}/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
# =============== End customer cannot modify confirmed order test seciton ===============


# =============== Start test admin permission section ===============
@pytest.mark.django_db
def test_admin_can_view_all_orders(api_client, admin, user, order):
    another_order = Order.objects.create(
        user=UserFactory(),
        total_price=200,
        order_status=Order.StatusChoices.PENDING,
        payment_status=Order.PaymentStatus.PENDING,
    )

    api_client.force_authenticate(user=admin)
    response = api_client.get("/api/orders/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
# =============== End test admin permission seciton ===============


# =============== Start test unauthenticated access section ===============
@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_order(api_client, product):
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 1,
            }
        ]
    }

    response = api_client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
# =============== End test unauthenticated access seciton ===============