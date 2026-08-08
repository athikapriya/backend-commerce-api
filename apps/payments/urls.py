from django.urls import path

from . import views

urlpatterns = [
    path("create-payment-intent/", views.CreatePaymentIntentAPIView.as_view(), name="create-payment-intent"),
    path("webhook/", views.StripeWebhookAPIView.as_view(), name="stripe-webhook"),
]
