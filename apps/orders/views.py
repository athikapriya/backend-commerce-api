from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import Order
from .serializers import OrderSerializer


# =============== Start OrderAPIView section ===============
@extend_schema(
    summary="List Orders",
    description=(
        "Returns orders for the authenticated user. "
        "Administrators receive all orders."
    ),
    tags=["Orders"],
)
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
@extend_schema(
    summary="Retrieve, Update or Delete Order",
    description=(
        "Retrieve an order by UUID. "
        "Customers can access only their own orders. "
        "Only administrators can update or delete orders."
    ),
    tags=["Orders"],
)
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