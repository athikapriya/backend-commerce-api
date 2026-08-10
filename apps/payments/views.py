from decimal import Decimal
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.orders.models import Order
from .serializers import CreatePaymentIntentSerializer, PaymentIntentResponseSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


# =============== Start CreatePaymentIntentAPIView section ===============
@extend_schema(
    summary="Create Stripe Payment Intent",
    description=(
        "Creates a Stripe PaymentIntent for an existing order. "
        "The authenticated user must own the order. "
        "Returns a Stripe client_secret which the frontend uses "
        "to complete the payment."
    ),
    tags=["Payments"],
    request=CreatePaymentIntentSerializer,
    responses={
        200: PaymentIntentResponseSerializer,
    },
)
class CreatePaymentIntentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]

        try:
            order = Order.objects.get(
                order_id = order_id,
                user = request.user,
            )
        except Order.DoesNotExist:
            return Response(
                {"detail" : "Order not found."},
                status = status.HTTP_404_NOT_FOUND,
            )

        if order.payment_status == Order.PaymentStatus.PAID:
            return Response(
                {"detail" : "This order has already been paid."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        if order.order_status == Order.StatusChoices.CANCELED:
            return Response(
                {"detail": "Canceled orders cannot be paid."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        if order.stripe_payment_intent_id:
            payment_intent = stripe.PaymentIntent.retrieve(
                order.stripe_payment_intent_id
            )
            return Response(
                {"client_secret": payment_intent.client_secret},
                status=status.HTTP_200_OK,
            )

        amount = int(order.total_price.quantize(Decimal("0.01")) * 100)
        payment_intent = stripe.PaymentIntent.create(
            amount = amount,
            currency = "usd",
            metadata={
                "order_id": str(order.order_id),
                "user_id": str(request.user.id),
            },
        )
        order.stripe_payment_intent_id = payment_intent.id
        order.save(update_fields=["stripe_payment_intent_id"])
        
        return Response(
            {"client_secret": payment_intent.client_secret},
            status=status.HTTP_200_OK,
        )
# =============== End CreatePaymentIntentAPIView seciton ===============


# =============== Start StripeWebhookAPIView section ===============
@extend_schema(
    summary="Stripe Webhook",
    description=(
        "Receives and verifies Stripe webhook events. "
        "Updates order payment status when a payment succeeds or fails."
    ),
    tags=["Payments"],
    request=None,
    responses={
        200: OpenApiResponse(
            description="Webhook received successfully."
        ),
    },
)
class StripeWebhookAPIView(APIView):
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except ValueError:
            return Response(
                {"detail": "Invalid payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except stripe.error.SignatureVerificationError:
            return Response(
                {"detail": "Invalid signature."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event_type = event["type"]

        if event_type == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]

            payment_intent_id = payment_intent["id"]

            try:
                order = Order.objects.get(
                    stripe_payment_intent_id=payment_intent_id
                )
            except Order.DoesNotExist:
                return Response(
                    {"detail": "Order not found. Event ignored."},
                    status=status.HTTP_200_OK,
                )

            order.payment_status = Order.PaymentStatus.PAID
            order.transaction_id = payment_intent_id
            order.order_status = Order.StatusChoices.CONFIRMED

            order.save(
                update_fields=[
                    "payment_status",
                    "transaction_id",
                    "order_status",
                    "updated_at",
                ]
            )

        elif event_type == "payment_intent.payment_failed":
            payment_intent = event["data"]["object"]

            payment_intent_id = payment_intent["id"]

            try:
                order = Order.objects.get(
                    stripe_payment_intent_id=payment_intent_id
                )
            except Order.DoesNotExist:
                return Response(
                    {"detail": "Order not found. Event ignored."},
                    status=status.HTTP_200_OK,
                )

            order.payment_status = Order.PaymentStatus.FAILED

            order.save(
                update_fields=[
                    "payment_status",
                    "updated_at",
                ]
            )

        return Response(
            {"detail": "Webhook received."},
            status=status.HTTP_200_OK,
        )
# =============== End StripeWebhookAPIView seciton ===============