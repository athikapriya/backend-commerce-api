from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import ProductSerializer
from .filters import ProductFilter
from .models import Product


# =============== Start Product Pagination section ===============
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 20
# =============== End Product Pagination seciton ===============


# =============== Start Product API View section ===============
class ProductAPIView(generics.ListCreateAPIView):
    
    queryset = Product.objects.filter(
        is_active=True,
        stock__gt=0
        ).select_related("category")
    
    serializer_class = ProductSerializer

    # ===== start pagination =====
    pagination_class = ProductPagination
    # ===== End pagination =====

    # ===== start Filtering, searching, ordering =====
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = ["name", "description", "category__name"]
    ordering_fields = [
        "price",
        "created_at",
        "name",
        "stock",
        ]
    
    ordering = ["-created_at"]
    # ===== End Filtering, searching, ordering =====
    
    # ===== start permissions =====
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    # ===== End permissions =====

# =============== End Product API View seciton ===============