from rest_framework import serializers


# =============== Start CreatePaymentIntentSerializer section ===============
class CreatePaymentIntentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
# =============== End CreatePaymentIntentSerializer seciton ===============