import pytest
import stripe
from unittest.mock import patch, MagicMock
from rest_framework import status

from apps.orders.models import Order
from factories import UserFactory

CREATE_PAYMENT_URL = "/api/payments/create-payment-intent/"
WEBHOOK_URL = "/api/payments/webhook/"


# =============== Start Test Successful PaymentIntent creation section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.PaymentIntent.create")
def test_customer_can_create_payment_intent(mock_create, api_client, user, order):
    api_client.force_authenticate(user=user)

    mock_payment_intent = MagicMock()
    mock_payment_intent.id = "pi_test_123"
    mock_payment_intent.client_secret = "pi_test_secret_123"

    mock_create.return_value = mock_payment_intent

    response = api_client.post(
        CREATE_PAYMENT_URL,
        {"order_id": str(order.order_id),},
        format="json",
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["client_secret"] == "pi_test_secret_123"

    order.refresh_from_db()
    assert order.stripe_payment_intent_id == "pi_test_123"

    mock_create.assert_called_once()
# =============== End Test Successful PaymentIntent creation seciton ===============


# =============== Start Testing amount sent to stripe section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.PaymentIntent.create")
def test_payment_intent_uses_correct_amount(mock_create, api_client, user, order):
    api_client.force_authenticate(user=user)

    mock_payment_intent = MagicMock()
    mock_payment_intent.id = "pi_test_amount"
    mock_payment_intent.client_secret = "secret"

    mock_create.return_value = mock_payment_intent

    response = api_client.post(
        CREATE_PAYMENT_URL,
        {"order_id": str(order.order_id)},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    mock_create.assert_called_once()

    call_kwargs = mock_create.call_args.kwargs

    assert call_kwargs["amount"] == 10000
    assert call_kwargs["currency"] == "usd"
# =============== End Testing amount sent to stripe seciton ===============


# =============== Start testing one customer cannot pay another user's order section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.PaymentIntent.create")
def test_customer_cannot_create_payment_for_another_users_order(mock_create, api_client, user, order):
    another_user = UserFactory()
    api_client.force_authenticate(user=another_user)

    response = api_client.post(
        CREATE_PAYMENT_URL,
        {"order_id": str(order.order_id)},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_create.assert_not_called()
# =============== End testing one customer cannot pay another user's order seciton ===============


# =============== Start Test already-paid orders section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.PaymentIntent.create")
def test_cannot_pay_already_paid_order(mock_create, api_client, user, order):
    order.payment_status = Order.PaymentStatus.PAID
    order.save(update_fields=["payment_status"])

    api_client.force_authenticate(user=user)

    response = api_client.post(
        CREATE_PAYMENT_URL,
        {"order_id": str(order.order_id)},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "This order has already been paid."
    mock_create.assert_not_called()
# =============== End Test already-paid orders seciton ===============


# =============== Start Test canceled orders section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.PaymentIntent.create")
def test_cannot_pay_canceled_order(mock_create, api_client, user, order):
    order.order_status = Order.StatusChoices.CANCELED
    order.save(update_fields=["order_status"])

    api_client.force_authenticate(user=user)

    response = api_client.post(
        CREATE_PAYMENT_URL,
        {"order_id": str(order.order_id)},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Canceled orders cannot be paid."
    mock_create.assert_not_called()
# =============== End Test canceled orders seciton ===============


# =============== Start Test successful Stripe payment section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.Webhook.construct_event")
def test_stripe_webhook_marks_order_as_paid(mock_construct_event, api_client, user, order):
    order.stripe_payment_intent_id = "pi_test_success"
    order.save(update_fields=["stripe_payment_intent_id"])

    mock_construct_event.return_value = {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {"id": "pi_test_success"}
        },
    }

    response = api_client.post(
        WEBHOOK_URL,
        data=b'{"test": "payload"}',
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test_signature",
    )

    assert response.status_code == status.HTTP_200_OK
    order.refresh_from_db()

    assert order.payment_status == Order.PaymentStatus.PAID
    assert order.order_status == Order.StatusChoices.CONFIRMED
    assert order.transaction_id == "pi_test_success"
# =============== End Test successful Stripe payment seciton ===============


# =============== Start Test failed payment section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.Webhook.construct_event")
def test_stripe_webhook_marks_order_as_failed(mock_construct_event, api_client, user, order):
    order.stripe_payment_intent_id = "pi_test_failed"
    order.save(update_fields=["stripe_payment_intent_id"])

    mock_construct_event.return_value = {
        "type": "payment_intent.payment_failed",
        "data": {
            "object": {"id": "pi_test_failed"}
        },
    }

    response = api_client.post(
        WEBHOOK_URL,
        data=b'{"test": "payload"}',
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test_signature",
    )
    assert response.status_code == status.HTTP_200_OK

    order.refresh_from_db()
    assert order.payment_status == Order.PaymentStatus.FAILED
# =============== End Test failed payment seciton ===============


# =============== Start Test invalid Stripe signature section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.Webhook.construct_event")
def test_stripe_webhook_rejects_invalid_signature(mock_construct_event, api_client):
    mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
        "Invalid signature",
        "test_signature",
    )

    response = api_client.post(
        WEBHOOK_URL,
        data=b'{"test": "payload"}',
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="invalid_signature",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Invalid signature."
# =============== End Test invalid Stripe signature seciton ===============


# =============== Start Test invalid payload section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.Webhook.construct_event")
def test_stripe_webhook_rejects_invalid_payload(mock_construct_event, api_client):
    mock_construct_event.side_effect = ValueError("Invalid payload")

    response = api_client.post(
        WEBHOOK_URL,
        data=b"invalid payload",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test_signature",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Invalid payload."
# =============== End Test invalid payload seciton ===============


# =============== Start Test unknown order section ===============
@pytest.mark.django_db
@patch("apps.payments.views.stripe.Webhook.construct_event")
def test_stripe_webhook_ignores_unknown_payment_intent(mock_construct_event, api_client):
    mock_construct_event.return_value = {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {"id": "pi_unknown"}
        },
    }

    response = api_client.post(
        WEBHOOK_URL,
        data=b'{"test": "payload"}',
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test_signature",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Order not found. Event ignored."
# =============== End Test unknown order seciton ===============