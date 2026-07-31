from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, viewsets, status

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .filters import OrderFilter


# =============== Start OrderViewSet section ===============
@extend_schema_view(
    list=extend_schema(
        summary="List Orders",
        description=(
            "Returns all orders. "
            "Customers can only see their own orders, "
            "while administrators can see every order. "
            "Supports filtering and ordering."
        ),
        tags=["Orders"],
    ),
    retrieve=extend_schema(
        summary="Retrieve Order",
        description=(
            "Retrieve a single order by its UUID. "
            "Customers can only retrieve their own orders."
        ),
        tags=["Orders"],
    ),
    create=extend_schema(
        summary="Create Order",
        description=(
            "Create a new order. "
            "Stock is validated before the order is created, "
            "product stock is reduced automatically, "
            "and the total price is calculated."
        ),
        tags=["Orders"],
    ),
    update=extend_schema(
        summary="Replace Order",
        description=(
            "Replace all order items. "
            "Only pending orders can have their items modified."
        ),
        tags=["Orders"],
    ),
    partial_update=extend_schema(
        summary="Partially Update Order",
        description=(
            "Update an order partially. "
            "Customers may modify items only while the order is pending. "
            "Administrators may update the order status."
        ),
        tags=["Orders"],
    ),
    destroy=extend_schema(
        summary="Delete Order",
        description="Only administrators can permanently delete an order.",
        tags=["Orders"],
    ),
)
class OrderviewSet(viewsets.ModelViewSet):
    throttle_scope = "orders"
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter

    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can delete orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)
# =============== End OrderViewSet seciton ===============