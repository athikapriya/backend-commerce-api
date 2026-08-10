from rest_framework import serializers


# =============== Start CreatePaymentIntentSerializer section ===============
class CreatePaymentIntentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
# =============== End CreatePaymentIntentSerializer seciton ===============


# =============== Start paymentIntentResponseSerializers section ===============
class PaymentIntentResponseSerializer(serializers.Serializer):
    client_secret = serializers.CharField()
# =============== End paymentIntentResponseSerializers seciton ===============