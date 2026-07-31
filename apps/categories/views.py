from rest_framework import generics
from django.db.models import Count
from drf_spectacular.utils import extend_schema

from .models import Category
from .serializers import CategorySerializer



# =============== Start Category API views section ===============
@extend_schema(
    summary="List Categories",
    description=(
        "Returns all parent categories with their child categories "
        "and the total number of products in each parent category."
    ),
    tags=["Categories"],
)
class CategoryAPIView(generics.ListAPIView):
    throttle_scope = "categories"
    queryset = Category.objects.filter(
        parent__isnull=True
        ).annotate(
            total_products=Count("children__products")
            ).prefetch_related("children")
    
    serializer_class = CategorySerializer
# =============== End Category API views seciton ===============