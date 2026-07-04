from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Order
from .serializers import OrderSerializer


# =============== Start OrderAPIView section ===============
class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.select_related("user").prefetch_related("items__product")

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
# =============== End OrderAPIView seciton ===============


# =============== Start OrderDetailsAPIView section ===============
class OrderDetailApIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    lookup_field = "order_id"

    def get_queryset(self):
        queryset = Order.objects.select_related("user").prefetch_related("items__product")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
    
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
# =============== End OrderDetailsAPIView seciton ===============